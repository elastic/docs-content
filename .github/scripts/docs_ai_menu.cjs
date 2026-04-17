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
    `^- \\[([ x])\\] ${escapeRegExp(label)} ${escapeRegExp(marker)}$`,
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
    '## Elastic Docs AI Menu',
    '',
    'Check one box to run an AI workflow for this issue.',
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
  isMenuComment,
  parseMenuState,
  buildMenuBody,
};
