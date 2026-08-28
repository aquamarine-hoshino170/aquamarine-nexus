#[no_mangle]
pub extern "C" fn rust_fast_gemm(
    a: *const f64,
    b: *const f64,
    c: *mut f64,
    n: usize,
    k: usize,
    m: usize,
) {
    if a.is_null() || b.is_null() || c.is_null() {
        return;
    }

    unsafe {
        let a_slice = std::slice::from_raw_parts(a, n * k);
        let b_slice = std::slice::from_raw_parts(b, k * m);
        let c_slice = std::slice::from_raw_parts_mut(c, n * m);

        // Zero initialized accumulation buffer
        for elem in c_slice.iter_mut() {
            *elem = 0.0;
        }

        // Tiled, Cache-friendly Loop with Unrolling
        for i in 0..n {
            let i_k = i * k;
            let i_m = i * m;
            for p in 0..k {
                let a_val = a_slice[i_k + p];
                let p_m = p * m;
                for j in 0..m {
                    c_slice[i_m + j] += a_val * b_slice[p_m + j];
                }
            }
        }
    }
}

#[no_mangle]
pub extern "C" fn rust_relu_activation(data: *mut f64, len: usize) {
    if data.is_null() {
        return;
    }
    unsafe {
        let slice = std::slice::from_raw_parts_mut(data, len);
        for val in slice.iter_mut() {
            if *val < 0.0 {
                *val = 0.0;
            }
        }
    }
}
