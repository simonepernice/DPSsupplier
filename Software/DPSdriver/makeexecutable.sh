#!/bin/bash
zip -r ../dps.zip * 
cd ..
echo '#!/usr/bin/env python' | cat - dps.zip > dpsinterface
chmod +x dpsinterface
rm dps.zip 
mv dpsinterface dist/ 
