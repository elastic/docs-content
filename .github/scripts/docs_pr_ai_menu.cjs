const MENU_START = '<!-- docs-pr-ai-menu:start -->';
const MENU_END = '<!-- docs-pr-ai-menu:end -->';

const WORKFLOW_CONFIG = {
  docsReview: {
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
    `^- \\[([ x])\\] ${escapeRegExp(label)} ${escapeRegExp(marker)}$`,
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
  };
}

function parseMenuState(body) {
  const state = {};

  for (const key of WORKFLOW_ORDER) {
    state[key] = parseWorkflowState(body, key);
  }

  return state;
}

function buildWorkflowLine(key, workflowState) {
  const { label, marker } = WORKFLOW_CONFIG[key];
  const selected = workflowState?.selected ? 'x' : ' ';

  return `- [${selected}] ${label} ${marker}`;
}

function buildMenuBody(state) {
  const normalizedState = state || {};

  return [
    MENU_START,
    '## Elastic Docs AI PR menu',
    '',
    'Check the box to run an AI review for this pull request.',
    '',
    ...WORKFLOW_ORDER.map((key) => buildWorkflowLine(key, normalizedState[key])),
    '',
    'Powered by GitHub Agentic Workflows and [docs-actions](https://github.com/elastic/docs-actions). For more information, reach out to the docs team.',
    '',
    MENU_END,
  ].join('\n');
}

module.exports = {
  MENU_START,
  MENU_END,
  WORKFLOW_ORDER,
  parseMenuState,
  buildMenuBody,
};
