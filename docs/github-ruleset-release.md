# GitHub ruleset: `release/*`

Blocks direct pushes to `release/*` and requires the fitness job (Climb 1 landing half). Apply with the GitHub Rulesets API. Do not push to `release/*` from a producer session. Create `release/*` branches only via [`.github/workflows/start-release.yml`](../.github/workflows/start-release.yml).

## Exact ruleset JSON

```json
{
  "name": "release-line-no-direct-push",
  "target": "branch",
  "enforcement": "active",
  "bypass_actors": [
    {
      "actor_id": 0,
      "actor_type": "Integration",
      "bypass_mode": "always"
    }
  ],
  "conditions": {
    "ref_name": {
      "include": ["refs/heads/release/*"],
      "exclude": []
    }
  },
  "rules": [
    {
      "type": "pull_request",
      "parameters": {
        "required_approving_review_count": 0,
        "dismiss_stale_reviews_on_push": false,
        "require_code_owner_review": false,
        "require_last_push_approval": false,
        "required_review_thread_resolution": false,
        "allowed_merge_methods": ["merge", "squash", "rebase"]
      }
    },
    {
      "type": "required_status_checks",
      "parameters": {
        "strict_required_status_checks_policy": true,
        "do_not_enforce_on_create": false,
        "required_status_checks": [
          {
            "context": "fitness",
            "integration_id": 15368
          }
        ]
      }
    },
    {
      "type": "non_fast_forward"
    }
  ]
}
```

`integration_id` `15368` is GitHub Actions (required check only). The required context is the `fitness` job in `.github/workflows/fitness.yml`.

The one `bypass_actors` entry is the start-release GitHub App (`actor_type` Integration). Replace `actor_id` `0` with that App's numeric App ID before applying. `GITHUB_TOKEN` and the GitHub Actions app cannot be this actor. `bypass_mode` is `always` so that App can create `release/*`; every other actor still needs a pull request for updates. `non_fast_forward` stays.

## Apply

The live ruleset id is `25824126`. After replacing `actor_id` `0`:

```bash
gh api --method PUT repos/Zygotic-AI/Natural-Language-Coding/rulesets/25824126 \
  --input docs/github-ruleset-release.json
```

The same body is saved at `docs/github-ruleset-release.json` for the API call.
