use hibitset::{BitIter, BitSet};
use pyo3::class::iter::{IterNextOutput, PyIterProtocol};
use pyo3::class::sequence::PySequenceProtocol;
use pyo3::prelude::*;

#[pyclass]
#[repr(transparent)]
struct PyBitSet(BitSet);

#[pyclass]
#[repr(transparent)]
struct PyBitSetIter(BitIter<BitSet>);

#[pymethods]
impl PyBitSet {
    #[new]
    fn new() -> Self {
        let set = BitSet::new();
        PyBitSet(set)
    }

    #[staticmethod]
    fn with_capacity(max: u32) -> Self {
        let set = BitSet::with_capacity(max);
        PyBitSet(set)
    }

    fn add(&mut self, item: u32) -> PyResult<bool> {
        Ok(self.0.add(item))
    }

    fn remove(&mut self, item: u32) -> PyResult<bool> {
        Ok(self.0.remove(item))
    }

    fn contains(&self, item: u32) -> PyResult<bool> {
        Ok(self.0.contains(item))
    }

    fn contains_set(&self, other: &Self) -> PyResult<bool> {
        Ok(self.0.contains_set(&other.0))
    }

    fn clear(&mut self) {
        self.0.clear()
    }
}

#[pyproto]
impl<'a> PySequenceProtocol<'a> for PyBitSet {
    fn __contains__(&'a self, item: u32) -> PyResult<bool> {
        self.contains(item)
    }
}

#[pyproto]
impl PyIterProtocol for PyBitSet {
    fn __iter__(slf: PyRefMut<Self>) -> PyBitSetIter {
        let clone: BitSet = slf.0.clone();
        PyBitSetIter(clone.into_iter())
    }
}

#[pyproto]
impl PyIterProtocol for PyBitSetIter {
    fn __iter__(slf: PyRef<Self>) -> PyRef<Self> {
        slf
    }

    fn __next__(mut slf: PyRefMut<Self>) -> IterNextOutput<u32, ()> {
        let next = slf.0.next();
        match next {
            Some(item) => IterNextOutput::Yield(item),
            None => IterNextOutput::Return(()),
        }
    }
}

#[pymodule]
fn pyhibitset(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<PyBitSet>()?;
    Ok(())
}
