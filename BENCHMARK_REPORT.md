# REPORT: PC-Miner Communication Benchmark

**Status**: ⚠️ FAILED (Throughput below expectations)
**Date**: 2025-12-16
**Hardware**: Lucky Miner LV06 (Reported as 'LuckyMiner BM1366')

## Results
- **Test Duration**: 30 seconds
- **Stratum Difficulty**: 1
- **Shares Received**: 1
- **Average Rate**: 0.03 Shares/sec
- **Effective Hashrate**: ~4 MH/s (at Pool side)

## Analysis
Despite setting `mining.set_difficulty` to 1, the miner is not flooding the server with shares as expected.
- **Expected Behavior**: >100 Shares/sec (for ~500 GH/s @ Diff 1)
- **Observed Behavior**: 1 Share total.

## Possible Causes
1. **Difficulty Ignored**: The miner might be ignoring the `set_difficulty` command and using a default high difficulty.
2. **Job Reject**: The miner might be rejecting the specific job format (empty coinbase, etc.) causing it to idle.
3. **Hardware Latency**: The miner might be stuck in a boot/initialization loop.

## Recommendation
- Verify strict Stratum compliance (e.g. `nBits` matching difficulty).
- Try `clean_jobs=True` explicitly in `mining.notify`.
- Test if `mining.configure` is required for this firmware version.
