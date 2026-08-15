export const PROJECT_CONFIG_URL = new URL('./project-config.json', import.meta.url);
let configPromise;

export function resolveProjectAsset(path) {
  return new URL(path, PROJECT_CONFIG_URL).href;
}

export async function loadProjectConfig() {
  if (!configPromise) {
    configPromise = fetch(PROJECT_CONFIG_URL, { cache: 'no-store' }).then(async response => {
      if (!response.ok) throw new Error(`Configuration V18 indisponible: HTTP ${response.status}`);
      const config = await response.json();
      if (config.version !== 'V18' || !config.model) throw new Error('Configuration V18 incohérente');
      window.__projectConfig = config;
      window.__projectConfigUrl = PROJECT_CONFIG_URL.href;
      return Object.freeze(config);
    });
  }
  return configPromise;
}

export function applyProjectVersion(config, root = document) {
  root.querySelectorAll('[data-project-version]').forEach(node => node.textContent = config.version);
  root.querySelectorAll('[data-project-release]').forEach(node => node.textContent = config.release);
  root.querySelectorAll('[data-project-source]').forEach(node => node.textContent = `SOURCE = ${config.viewerSource}`);
  root.documentElement.dataset.projectVersion = config.version;
  root.documentElement.dataset.projectRelease = config.release;
}
