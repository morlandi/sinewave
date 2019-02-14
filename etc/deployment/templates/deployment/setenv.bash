#!/bin/bash
source {{project.pythonpath}}/activate
cd {{project.website_home}}
echo 'PYTHON:' `which python`
