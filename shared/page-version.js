import { loadProjectConfig, applyProjectVersion } from './project-config.js?release=v18-live-sync-4';

try {
  const config = await loadProjectConfig();
  applyProjectVersion(config);
  window.__projectConfigReady = true;
} catch (error) {
  window.__projectConfigFailed = true;
  console.error('[V18 project-config]', error);
}
