#!/bin/bash
export PYTHONPATH=${WORKSPACE}/tests/checker/plugins:${PYTHONPATH}
CHECK="*.py pixo* ui_elements preflight scenegraph"

IGNORE="shotgun_api3,libs,yaml,i18n,QColorScheme,pixopipe.pro,pixoLibs/scenebuilder"
echo $PYTHONPATH
CMD="pylint --ignore=${IGNORE}  --rcfile=${WORKSPACE}/tests/checker/pylintrc ${CHECK}"
echo $CMD
$CMD