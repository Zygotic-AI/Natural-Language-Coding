# assert_sign_adrs_script_passes

CI-less run of `scripts/sign-adrs.sh` (thin entry; policy in `goals/sign_adrs/execute.sh`) with a throwaway test key (`--test-fingerprint` + `--allow-test-key` only). Proves one upfront unlock, signs only missing or stale ADRs, and is idempotent on a second run.
