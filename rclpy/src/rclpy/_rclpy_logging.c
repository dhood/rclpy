// Copyright 2017 Open Source Robotics Foundation, Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include <Python.h>

#include <rcutils/logging.h>

/// Initialize the logging system.
/**
 * \return None
 */
static PyObject *
rclpy_logging_initialize()
{
  rcutils_logging_initialize();
  Py_RETURN_NONE;
}

/// Set the global severity threshold of the logging system.
/**
 *
 * \param[in] severity Threshold to set
 * \return None, or
 * \return NULL on failure
 */
static PyObject *
rclpy_logging_set_severity_threshold(PyObject * Py_UNUSED(module), PyObject * args)
{
  int severity;
  if (!PyArg_ParseTuple(args, "i", &severity)) {
    return NULL;
  }

  rcutils_logging_set_severity_threshold(severity);
  Py_RETURN_NONE;
}

/// Get the global severity threshold of the logging system.
/**
 * \return severity
 */
static PyObject *
rclpy_logging_get_severity_threshold()
{
  int severity = rcutils_logging_get_severity_threshold();

  return PyLong_FromLong(severity);
}

/// Define the public methods of this module
static PyMethodDef rclpy_logging_methods[] = {
  {"rclpy_logging_initialize", rclpy_logging_initialize, METH_NOARGS,
   "Initialize the logging system."},
  {"rclpy_logging_get_severity_threshold", rclpy_logging_get_severity_threshold, METH_NOARGS,
   "Get the global severity threshold."},
  {"rclpy_logging_set_severity_threshold", rclpy_logging_set_severity_threshold, METH_VARARGS,
   "Set the global severity threshold."},

  {NULL, NULL, 0, NULL}  /* sentinel */
};

/// Define the Python module
static struct PyModuleDef _rclpy_logging_module = {
  PyModuleDef_HEAD_INIT,
  "_rclpy_logging",
  "_rclpy_logging_doc",
  -1,   /* -1 means that the module keeps state in global variables */
  rclpy_logging_methods,
  NULL,
  NULL,
  NULL,
  NULL
};

/// Init function of this module
PyMODINIT_FUNC PyInit__rclpy_logging(void)
{
  return PyModule_Create(&_rclpy_logging_module);
}