# assert_adr_detached_sig_fails

Known-bad and known-good for per-file ADR detached signatures (ADR 0056):

- valid signature by the pinned key → MET
- (a) ADR edited after signing → NOT_MET
- (b) signature by a different key → NOT_MET
- (c) missing signature → NOT_MET
- (d) batch statement present but no per-file signature → NOT_MET
