#!/usr/bin/env bash
# Owner catch-up: detached-sign every numbered ADR whose sibling signature is
# missing or does not verify against the current file bytes.
#
# Convention (ADR 0056): adrs/NNNN-slug.md  ->  adrs/NNNN-slug.md.asc
# Default key: 9D1BD57770FC3A1DE84702750AFD22B063AE01BC (Ed25519).
#
# The owner runs this locally (once for catch-up, then per release).
# Passphrase prompt: at most once per run. Before any ADR is signed, the script
# unlocks the pinned key by detach-signing a throwaway string to /dev/null.
# gpg-agent caches that unlock for default-cache-ttl (GnuPG default 600 seconds;
# see gpg-agent.conf). That cache must cover the signing loop. After unlock,
# each ADR sign uses --pinentry-mode error so a second prompt is a hard refuse.
# This script never stores a passphrase.
# Optional loopback pinentry on the unlock only:
#   NLC_SIGN_ADRS_PINENTRY_LOOPBACK=1
# (still does not store the passphrase; gpg reads it from pinentry).
#
# --test-fingerprint is for automated tests only. It requires --allow-test-key.
# CI (GITHUB_ACTIONS or CI=true) is refused unless --ci-less is passed.
set -euo pipefail

DEFAULT_FINGERPRINT="9D1BD57770FC3A1DE84702750AFD22B063AE01BC"

ROOT=""
ADR_DIR=""
FINGERPRINT="$DEFAULT_FINGERPRINT"
DRY_RUN=0
GIT_ADD=0
CI_LESS=0
TEST_FINGERPRINT=""
ALLOW_TEST_KEY=0

usage() {
  cat <<'EOF'
Usage: scripts/sign-adrs.sh [options]

  --dry-run                 Print what would be signed; do not invoke gpg --sign
  --git-add                 Stage newly written or refreshed *.md.asc files
  --ci-less                 Allow running when CI/GITHUB_ACTIONS is set (tests)
  --test-fingerprint FPR    Override signing key (tests only; needs --allow-test-key)
  --allow-test-key          Required together with --test-fingerprint
  --root DIR                Repository root (default: parent of scripts/)
  --adr-dir DIR             ADR directory (default: <root>/adrs)
  -h, --help                Show this help

Environment:
  NLC_SIGN_ADRS_PINENTRY_LOOPBACK=1   Unlock step uses --pinentry-mode loopback
  GNUPGHOME                           Honored by gpg (tests set a throwaway home)

Passphrase: prompted at most once (upfront unlock). gpg-agent default-cache-ttl
must cover the run; a later sign that would prompt again is refused.

After a real owner run: commit and push the .asc files (or re-run with --git-add).
EOF
}

die() {
  echo "SIGN-ADRS:REFUSE $*" >&2
  exit 2
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=1; shift ;;
    --git-add) GIT_ADD=1; shift ;;
    --ci-less) CI_LESS=1; shift ;;
    --allow-test-key) ALLOW_TEST_KEY=1; shift ;;
    --test-fingerprint)
      [[ $# -ge 2 ]] || die "--test-fingerprint needs a fingerprint"
      TEST_FINGERPRINT="$2"
      shift 2
      ;;
    --root)
      [[ $# -ge 2 ]] || die "--root needs a directory"
      ROOT="$2"
      shift 2
      ;;
    --adr-dir)
      [[ $# -ge 2 ]] || die "--adr-dir needs a directory"
      ADR_DIR="$2"
      shift 2
      ;;
    -h|--help) usage; exit 0 ;;
    *) die "unknown argument: $1" ;;
  esac
done

if [[ -n "${GITHUB_ACTIONS:-}" || "${CI:-}" == "true" ]] && [[ "$CI_LESS" -eq 0 ]]; then
  die "refusing to create signatures in CI; owner runs this locally (or pass --ci-less in tests)"
fi

if [[ -n "$TEST_FINGERPRINT" && "$ALLOW_TEST_KEY" -eq 0 ]]; then
  die "--test-fingerprint is for tests only; pass --allow-test-key"
fi
if [[ "$ALLOW_TEST_KEY" -eq 1 && -z "$TEST_FINGERPRINT" ]]; then
  die "--allow-test-key requires --test-fingerprint"
fi
if [[ -n "$TEST_FINGERPRINT" ]]; then
  FINGERPRINT="$(printf '%s' "$TEST_FINGERPRINT" | tr -d '[:space:]' | tr '[:lower:]' '[:upper:]')"
  echo "SIGN-ADRS:WARN using --test-fingerprint (tests only)" >&2
fi

if [[ -z "$ROOT" ]]; then
  ROOT="$(cd "$(dirname "$0")/.." && pwd)"
fi
ROOT="$(cd "$ROOT" && pwd)"
if [[ -z "$ADR_DIR" ]]; then
  ADR_DIR="${ROOT}/adrs"
fi
[[ -d "$ADR_DIR" ]] || die "ADR directory missing: $ADR_DIR"

command -v gpg >/dev/null 2>&1 || die "gpg not found"

normalize_fpr() {
  printf '%s' "$1" | tr -d '[:space:]' | tr '[:lower:]' '[:upper:]'
}

FINGERPRINT="$(normalize_fpr "$FINGERPRINT")"
[[ ${#FINGERPRINT} -ge 16 ]] || die "fingerprint looks empty"

if ! gpg --batch --list-secret-keys --with-colons "$FINGERPRINT" 2>/dev/null | grep -q '^sec:'; then
  die "signing key $FINGERPRINT is not in the local keyring"
fi

gpg_pinentry_args=()
if [[ -n "${NLC_SIGN_ADRS_PINENTRY_LOOPBACK:-}" ]]; then
  gpg_pinentry_args+=(--pinentry-mode loopback)
fi

sig_path_for() {
  printf '%s.asc' "$1"
}

# Return 0 when the sibling detached signature verifies as VALIDSIG by FINGERPRINT
# over the exact current bytes of the ADR file.
sig_ok() {
  local doc="$1"
  local sig
  sig="$(sig_path_for "$doc")"
  [[ -f "$sig" ]] || return 1
  local status
  status="$(gpg --batch --status-fd 2 --verify "$sig" "$doc" 2>&1 >/dev/null || true)"
  local line fpr
  local good=0
  while IFS= read -r line; do
    case "$line" in
      "[GNUPG:] VALIDSIG "*)
        fpr="$(normalize_fpr "${line##* }")"
        if [[ "$fpr" == "$FINGERPRINT" ]]; then
          good=1
        fi
        ;;
    esac
  done <<<"$status"
  [[ "$good" -eq 1 ]]
}

mapfile -t ADRS < <(find "$ADR_DIR" -maxdepth 1 -type f -name '[0-9][0-9][0-9][0-9]-*.md' | sort)
[[ ${#ADRS[@]} -gt 0 ]] || die "no numbered ADR files under $ADR_DIR"

need=()
fresh=()
for doc in "${ADRS[@]}"; do
  if sig_ok "$doc"; then
    fresh+=("$doc")
  else
    need+=("$doc")
  fi
done

echo "SIGN-ADRS: scanned ${#ADRS[@]} numbered ADR(s) under $ADR_DIR"
echo "SIGN-ADRS: already valid ${#fresh[@]}"
echo "SIGN-ADRS: missing or stale ${#need[@]}"

if [[ "$DRY_RUN" -eq 1 ]]; then
  for doc in "${need[@]}"; do
    echo "SIGN-ADRS:DRY-RUN would sign $doc -> $(sig_path_for "$doc")"
  done
  echo "SIGN-ADRS:DRY-RUN ${#need[@]} file(s) would be signed with $FINGERPRINT"
  exit 0
fi

if [[ ${#need[@]} -eq 0 ]]; then
  echo "SIGN-ADRS:MET nothing to sign (idempotent)"
  echo "Next: no new .asc files. If this was catch-up, the signatures are already committed."
  exit 0
fi

# One unlock for the whole run. Pinentry may prompt here, and only here.
# gpg-agent then caches the passphrase for default-cache-ttl (default 600s).
gpg-connect-agent /bye >/dev/null 2>&1 || true
echo "SIGN-ADRS:UNLOCK signing throwaway to /dev/null so gpg-agent caches the key"
echo "SIGN-ADRS:UNLOCK default-cache-ttl (GnuPG default 600s) must cover this run"
if ! printf '%s\n' "nlc-sign-adrs-unlock" | gpg --yes --local-user "$FINGERPRINT" \
  --detach-sign --armor "${gpg_pinentry_args[@]}" --output /dev/null; then
  die "upfront unlock failed; the passphrase was not cached. Refusing rather than prompting again."
fi
echo "SIGN-ADRS:UNLOCK cached; ADR signs use --pinentry-mode error (no second prompt)"

signed=()
for doc in "${need[@]}"; do
  sig="$(sig_path_for "$doc")"
  rm -f "$sig"
  status=""
  if ! status="$(gpg --batch --yes --local-user "$FINGERPRINT" --detach-sign --armor \
    --pinentry-mode error --status-fd 2 \
    --output "$sig" "$doc" 2>&1)"; then
    if printf '%s\n' "$status" | grep -q 'NEED_PASSPHRASE\|PINENTRY_LAUNCHED\|pinentry'; then
      die "signing $doc would require another passphrase prompt. gpg-agent cache (default-cache-ttl, GnuPG default 600s) must cover the whole run. Re-run the script; a prompt must not recur."
    fi
    die "gpg --detach-sign failed for $doc (pinentry-mode error; no second prompt): ${status}"
  fi
  if printf '%s\n' "$status" | grep -q 'PINENTRY_LAUNCHED'; then
    die "signing $doc launched pinentry after unlock. A prompt must not recur."
  fi
  if ! sig_ok "$doc"; then
    die "gpg produced a signature that does not verify for $doc"
  fi
  echo "SIGN-ADRS:SIGNED $doc -> $sig"
  signed+=("$sig")
done

echo "SIGN-ADRS:MET signed ${#signed[@]} ADR(s); skipped ${#fresh[@]} already valid"

if [[ "$GIT_ADD" -eq 1 ]]; then
  (
    cd "$ROOT"
    git add -- "${signed[@]}"
  )
  echo "SIGN-ADRS: staged ${#signed[@]} .asc file(s). Commit and push on your branch."
else
  echo "Next: commit and push the new .asc files, or re-run with --git-add to stage them:"
  for sig in "${signed[@]}"; do
    echo "  $sig"
  done
fi
