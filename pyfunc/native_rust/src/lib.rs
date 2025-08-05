use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

#[pyfunction]
fn median(mut data: Vec<f64>) -> PyResult<f64> {
    if data.is_empty() {
        return Err(pyo3::exceptions::PyValueError::new_err("median() arg is an empty sequence"));
    }

    data.sort_by(|a, b| a.partial_cmp(b).unwrap());

    let mid = data.len() / 2;
    if data.len() % 2 == 0 {
        Ok((data[mid - 1] + data[mid]) / 2.0)
    } else {
        Ok(data[mid])
    }
}

#[pyfunction]
fn stdev(data: Vec<f64>) -> PyResult<f64> {
    let n = data.len();
    if n < 2 {
        return Err(pyo3::exceptions::PyValueError::new_err("stdev() requires at least two data points"));
    }

    let mean = data.iter().sum::<f64>() / n as f64;
    let variance = data.iter().map(|value| {
        let diff = mean - value;
        diff * diff
    }).sum::<f64>() / n as f64;

    Ok(variance.sqrt())
}

#[pymodule]
fn native_rust(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(median, m)?)?;
    m.add_function(wrap_pyfunction!(stdev, m)?)?;
    Ok(())
}