
// this file has the param overrides for the default environment
local base = import './base.libsonnet';

base {
  components +: {
    smokeTestImage: 'docker-test.repo.splunkdev.net/user-icorrales/security-content-test',
    serviceAccountName: "sa-tr-staging",
    vaultReadPath: 'scpauth-stage1/token/threat-research-test.app-stage1',
    tenant: 'research',
    dspEnv: 'staging',
  }
}
