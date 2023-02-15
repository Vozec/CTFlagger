#!/bin/bash

runuser -l server -c "cd ${DOCUMENT_ROOT};python3 ${DOCUMENT_ROOT}/app.py"
