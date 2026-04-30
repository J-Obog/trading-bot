import { renderHome } from './js/pages/home.js';
import { renderAnalyst } from './js/pages/analyst.js';
import { renderLeaderboard } from './js/pages/leaderboard.js';
import { renderTicker } from './js/pages/ticker.js';

const routes = {
  '/': renderHome,
  '/analyst': renderAnalyst,
  '/leaderboard': renderLeaderboard,
  '/ticker': renderTicker,
};

function router() {
  const path = window.location.pathname;
  const page = routes[path] || renderHome;
  page(document.getElementById('app'));
}

document.addEventListener('click', e => {
  if (e.target.matches('[data-link]')) {
    e.preventDefault();
    history.pushState(null, '', e.target.href);
    router();
  }
});

window.addEventListener('popstate', router);

router();
