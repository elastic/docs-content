const MENU_START = '<!-- docs-pr-ai-menu:start -->';
const MENU_END = '<!-- docs-pr-ai-menu:end -->';

const WORKFLOW_CONFIG = {
  docsReview: {
    checkNamePrefix: 'Docs AI / docs review',
    label: 'Review docs changes ([`docs-review`](https://github.com/elastic/docs-actions/blob/main/.github/workflows/gh-aw-docs-review.md)).',
    marker: '<!-- docs-pr-ai-menu:docs-review -->',
  },
};

const WORKFLOW_ORDER = ['docsReview'];

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function getLinePattern(key) {
  const { label, marker } = WORKFLOW_CONFIG[key];

  return new RegExp(
    `^- \\[([ x])\\] ${escapeRegExp(label)}(?: (Status: .*?))? ${escapeRegExp(marker)}$`,
    'm'
  );
}

function parseWorkflowState(body, key) {
  const match = (body || '').match(getLinePattern(key));

  if (!match) {
    return {
      selected: false,
    };
  }

  return {
    selected: match[1] === 'x',
    statusText: match[2] || null,
  };
}

function parseMenuState(body) {
  const state = {};

  for (const key of WORKFLOW_ORDER) {
    state[key] = parseWorkflowState(body, key);
  }

  return state;
}

function getStatusText(workflowState, workflowStatus) {
  if (workflowStatus?.statusText) {
    return workflowStatus.statusText;
  }

  const progressLink = workflowStatus?.detailsUrl
    ? ` [View progress](${workflowStatus.detailsUrl}).`
    : '';

  if (workflowStatus?.status === 'in_progress' || workflowStatus?.status === 'queued') {
    return `Status: running.${progressLink}`;
  }

  if (workflowStatus?.status === 'completed') {
    if (workflowStatus.conclusion === 'success') {
      const outcome = workflowStatus.outcome === 'no-findings' ? ', no findings' : '';
      return `Status: completed${outcome}.${progressLink}`;
    }

    if (workflowStatus.conclusion === 'cancelled') {
      return `Status: cancelled.${progressLink}`;
    }

    return `Status: needs attention.${progressLink}`;
  }

  // A refresh without an override, for example after a push, must not reset a finished run to "queued".
  const existingStatus = workflowState?.statusText;
  if (workflowState?.selected && existingStatus && !/^Status: (not started|queued)\./.test(existingStatus)) {
    return existingStatus;
  }

  if (workflowState?.selected) {
    return 'Status: queued.';
  }

  return 'Status: not started.';
}

function getWorkflowStatusFromCheckRuns(key, checkRuns) {
  const { checkNamePrefix } = WORKFLOW_CONFIG[key];
  const matchingCheckRuns = (checkRuns || []).filter((checkRun) =>
    checkRun.name?.startsWith(checkNamePrefix) &&
    checkRun.conclusion !== 'skipped'
  );

  if (matchingCheckRuns.length === 0) {
    return null;
  }

  matchingCheckRuns.sort((left, right) =>
    new Date(right.started_at || right.created_at || 0) - new Date(left.started_at || left.created_at || 0)
  );

  return {
    conclusion: matchingCheckRuns[0].conclusion,
    detailsUrl: matchingCheckRuns[0].details_url,
    status: matchingCheckRuns[0].status,
  };
}

const DOCS_REVIEW_SUMMARY_HEADING = '## Docs review summary';

// The review workflow submits a PR review when it has findings. With no findings it posts the summary
// as a regular PR comment instead. Neither means that no summary is visible (for example, a noop).
async function getDocsReviewOutcome({ github, context, pullRequestNumber, since }) {
  const sinceTime = new Date(since).getTime();

  if (Number.isNaN(sinceTime)) {
    return null;
  }

  const { owner, repo } = context.repo;
  const isBot = (item) => item.user?.login === 'github-actions[bot]';

  const reviews = await github.paginate(github.rest.pulls.listReviews, {
    owner,
    repo,
    pull_number: pullRequestNumber,
    per_page: 100,
  });

  if (reviews.some((review) => isBot(review) && new Date(review.submitted_at).getTime() >= sinceTime)) {
    return 'findings';
  }

  const comments = await github.paginate(github.rest.issues.listComments, {
    owner,
    repo,
    issue_number: pullRequestNumber,
    per_page: 100,
  });

  if (comments.some((comment) =>
    isBot(comment) &&
    new Date(comment.created_at).getTime() >= sinceTime &&
    comment.body?.startsWith(DOCS_REVIEW_SUMMARY_HEADING)
  )) {
    return 'no-findings';
  }

  return null;
}

function buildWorkflowLine(key, workflowState, workflowStatus) {
  const { label, marker } = WORKFLOW_CONFIG[key];
  const selected = workflowState?.selected ? 'x' : ' ';
  const statusText = getStatusText(workflowState, workflowStatus);

  return `- [${selected}] ${label} ${statusText} ${marker}`;
}

function buildMenuBody(state, statuses) {
  const normalizedState = state || {};
  const normalizedStatuses = statuses || {};

  return [
    MENU_START,
    '## Elastic Docs AI PR menu',
    '',
    'Check the box to run an AI review for this pull request.',
    '',
    ...WORKFLOW_ORDER.map((key) =>
      buildWorkflowLine(key, normalizedState[key], normalizedStatuses[key])
    ),
    '',
    'Powered by GitHub Agentic Workflows and [docs-actions](https://github.com/elastic/docs-actions). For more information, reach out to the docs team.',
    '',
    MENU_END,
  ].join('\n');
}

async function getCheckRunsForPullRequest(github, context, pullRequestNumber) {
  const { data: pullRequest } = await github.rest.pulls.get({
    owner: context.repo.owner,
    repo: context.repo.repo,
    pull_number: pullRequestNumber,
  });

  const { data: checks } = await github.rest.checks.listForRef({
    owner: context.repo.owner,
    repo: context.repo.repo,
    ref: pullRequest.head.sha,
    per_page: 100,
  });

  return checks.check_runs || [];
}

async function findMenuComment(github, context, pullRequestNumber) {
  const { data: comments } = await github.rest.issues.listComments({
    owner: context.repo.owner,
    repo: context.repo.repo,
    issue_number: pullRequestNumber,
    per_page: 100,
  });

  return comments.find((comment) =>
    comment.user?.login === 'github-actions[bot]' &&
    comment.body?.includes(MENU_START) &&
    comment.body?.includes(MENU_END)
  );
}

function getActiveWorkflowStatusFromState(workflowState) {
  if (workflowState?.statusText?.startsWith('Status: running.')) {
    return {
      statusText: workflowState.statusText,
    };
  }

  return null;
}

function buildWorkflowStatuses(checkRuns, statusOverrides, existingState) {
  return Object.fromEntries(
    WORKFLOW_ORDER.map((key) => [
      key,
      statusOverrides?.[key] ||
        getWorkflowStatusFromCheckRuns(key, checkRuns) ||
        getActiveWorkflowStatusFromState(existingState?.[key]),
    ])
  );
}

async function upsertMenuComment({
  core,
  createIfMissing = true,
  github,
  context,
  pullRequestNumber,
  statusOverrides,
}) {
  const checkRuns = await getCheckRunsForPullRequest(github, context, pullRequestNumber);
  const existingComment = await findMenuComment(github, context, pullRequestNumber);

  if (!existingComment && !createIfMissing) {
    core?.warning('AI PR menu comment was not found.');
    return;
  }

  const existingState = parseMenuState(existingComment?.body || '');
  const docsReviewOverride = statusOverrides?.docsReview;

  if (docsReviewOverride?.status === 'completed' && docsReviewOverride.conclusion === 'success' && !docsReviewOverride.outcome) {
    try {
      const outcome = await getDocsReviewOutcome({
        github,
        context,
        pullRequestNumber,
        since: context.payload?.comment?.updated_at,
      });
      statusOverrides = { ...statusOverrides, docsReview: { ...docsReviewOverride, outcome } };
    } catch (error) {
      core?.warning(`Could not classify the docs review outcome: ${error.message}`);
    }
  }

  const statuses = buildWorkflowStatuses(checkRuns, statusOverrides, existingState);
  const body = buildMenuBody(existingState, statuses);

  if (existingComment) {
    await github.rest.issues.updateComment({
      owner: context.repo.owner,
      repo: context.repo.repo,
      comment_id: existingComment.id,
      body,
    });
    return;
  }

  await github.rest.issues.createComment({
    owner: context.repo.owner,
    repo: context.repo.repo,
    issue_number: pullRequestNumber,
    body,
  });
}

module.exports = {
  MENU_START,
  MENU_END,
  WORKFLOW_ORDER,
  parseMenuState,
  getWorkflowStatusFromCheckRuns,
  getDocsReviewOutcome,
  buildMenuBody,
  upsertMenuComment,
};
