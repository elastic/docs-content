const MENU_START = '<!-- docs-ai-menu:start -->';
const MENU_END = '<!-- docs-ai-menu:end -->';

const WORKFLOW_CONFIG = {
  triage: {
    label: 'Triage ([`docs-triage`](https://github.com/elastic/docs-actions/blob/main/.github/workflows/gh-aw-issue-triage.md)).',
    marker: '<!-- docs-ai-menu:triage -->',
  },
  issueScope: {
    label: 'Scope the docs work ([`docs-issue-scope`](https://github.com/elastic/docs-actions/blob/main/.github/workflows/gh-aw-docs-issue-scope.md)).',
    marker: '<!-- docs-ai-menu:issue-scope -->',
  },
};

const WORKFLOW_ORDER = ['triage', 'issueScope'];

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

function isMenuComment(body) {
  return (body || '').includes(MENU_START) && (body || '').includes(MENU_END);
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
      return `Status: completed.${progressLink}`;
    }

    if (workflowStatus.conclusion === 'cancelled') {
      return `Status: cancelled.${progressLink}`;
    }

    return `Status: needs attention.${progressLink}`;
  }

  if (workflowState?.statusText) {
    return workflowState.statusText;
  }

  if (workflowState?.selected) {
    return 'Status: queued.';
  }

  return 'Status: not started.';
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
    '## Elastic Docs AI Menu',
    '',
    'Check one box to run an AI workflow for this issue.',
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

async function findMenuComment(github, context, issueNumber) {
  const { data: comments } = await github.rest.issues.listComments({
    owner: context.repo.owner,
    repo: context.repo.repo,
    issue_number: issueNumber,
    per_page: 100,
  });

  return comments.find((comment) =>
    comment.user?.login === 'github-actions[bot]' &&
    isMenuComment(comment.body)
  );
}

function buildWorkflowStatuses(existingState, statusOverrides) {
  return Object.fromEntries(
    WORKFLOW_ORDER.map((key) => [
      key,
      statusOverrides?.[key] || {
        statusText: existingState?.[key]?.statusText,
      },
    ])
  );
}

async function upsertMenuComment({
  core,
  createIfMissing = true,
  github,
  context,
  issueNumber,
  statusOverrides,
}) {
  const existingComment = await findMenuComment(github, context, issueNumber);

  if (!existingComment && !createIfMissing) {
    core?.warning('AI menu comment was not found.');
    return;
  }

  const existingState = parseMenuState(existingComment?.body || '');
  const statuses = buildWorkflowStatuses(existingState, statusOverrides);
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
    issue_number: issueNumber,
    body,
  });
}

module.exports = {
  MENU_START,
  MENU_END,
  WORKFLOW_ORDER,
  isMenuComment,
  parseMenuState,
  buildMenuBody,
  upsertMenuComment,
};
