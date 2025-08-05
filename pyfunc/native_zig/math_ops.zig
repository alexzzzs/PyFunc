const std = @import("std");
const math = std.math;

// Export functions for Python FFI
export fn zig_sum_f64(data: [*]f64, size: usize) f64 {
    var sum: f64 = 0.0;
    for (0..size) |i| {
        sum += data[i];
    }
    return sum;
}

export fn zig_sum_i32(data: [*]i32, size: usize) i64 {
    var sum: i64 = 0;
    for (0..size) |i| {
        sum += data[i];
    }
    return sum;
}

export fn zig_mean_f64(data: [*]f64, size: usize) f64 {
    if (size == 0) return 0.0;
    return zig_sum_f64(data, size) / @as(f64, @floatFromInt(size));
}

export fn zig_min_f64(data: [*]f64, size: usize) f64 {
    if (size == 0) return 0.0;
    var min_val = data[0];
    for (1..size) |i| {
        if (data[i] < min_val) {
            min_val = data[i];
        }
    }
    return min_val;
}

export fn zig_max_f64(data: [*]f64, size: usize) f64 {
    if (size == 0) return 0.0;
    var max_val = data[0];
    for (1..size) |i| {
        if (data[i] > max_val) {
            max_val = data[i];
        }
    }
    return max_val;
}

export fn zig_variance_f64(data: [*]f64, size: usize) f64 {
    if (size < 2) return 0.0;
    
    const mean = zig_mean_f64(data, size);
    var variance: f64 = 0.0;
    
    for (0..size) |i| {
        const diff = data[i] - mean;
        variance += diff * diff;
    }
    
    return variance / @as(f64, @floatFromInt(size));
}

export fn zig_std_dev_f64(data: [*]f64, size: usize) f64 {
    return math.sqrt(zig_variance_f64(data, size));
}

// Fast mathematical operations
export fn zig_map_multiply_f64(data: [*]f64, size: usize, multiplier: f64) void {
    for (0..size) |i| {
        data[i] *= multiplier;
    }
}

export fn zig_map_add_f64(data: [*]f64, size: usize, addend: f64) void {
    for (0..size) |i| {
        data[i] += addend;
    }
}

export fn zig_map_power_f64(data: [*]f64, size: usize, exponent: f64) void {
    for (0..size) |i| {
        data[i] = math.pow(f64, data[i], exponent);
    }
}

// Vector operations
export fn zig_dot_product_f64(a: [*]f64, b: [*]f64, size: usize) f64 {
    var result: f64 = 0.0;
    for (0..size) |i| {
        result += a[i] * b[i];
    }
    return result;
}

export fn zig_vector_magnitude_f64(data: [*]f64, size: usize) f64 {
    var sum_squares: f64 = 0.0;
    for (0..size) |i| {
        sum_squares += data[i] * data[i];
    }
    return math.sqrt(sum_squares);
}

// Fast filtering (returns count of elements that pass)
export fn zig_count_greater_than_f64(data: [*]f64, size: usize, threshold: f64) usize {
    var count: usize = 0;
    for (0..size) |i| {
        if (data[i] > threshold) {
            count += 1;
        }
    }
    return count;
}

// Cumulative operations
export fn zig_cumsum_f64(data: [*]f64, size: usize) void {
    for (1..size) |i| {
        data[i] += data[i - 1];
    }
}

export fn zig_diff_f64(data: [*]f64, size: usize) void {
    if (size < 2) return;
    
    var i = size - 1;
    while (i > 0) : (i -= 1) {
        data[i] = data[i] - data[i - 1];
    }
    data[0] = 0.0; // First element becomes 0
}

// Batch operations to reduce FFI overhead
export fn zig_batch_stats_f64(data: [*]f64, size: usize, results: [*]f64) void {
    // Calculate multiple statistics in one call
    results[0] = zig_sum_f64(data, size);        // sum
    results[1] = zig_mean_f64(data, size);       // mean
    results[2] = zig_min_f64(data, size);        // min
    results[3] = zig_max_f64(data, size);        // max
    results[4] = zig_std_dev_f64(data, size);    // stdev
}

export fn zig_batch_basic_f64(data: [*]f64, size: usize, results: [*]f64) void {
    // Calculate basic statistics (faster subset)
    results[0] = zig_sum_f64(data, size);        // sum
    results[1] = zig_mean_f64(data, size);       // mean
    results[2] = zig_min_f64(data, size);        // min
    results[3] = zig_max_f64(data, size);        // max
}