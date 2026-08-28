#include <stdlib.h>

void c_gemm_fast(const double* A, const double* B, double* C, int N, int K, int M) {
    for (int i = 0; i < N; ++i) {
        int iK = i * K;
        int iM = i * M;
        for (int k = 0; k < K; ++k) {
            double a_val = A[iK + k];
            int kM = k * M;
            for (int j = 0; j < M; ++j) {
                C[iM + j] += a_val * B[kM + j];
            }
        }
    }
}
