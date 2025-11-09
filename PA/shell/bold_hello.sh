#!/bin/bash
# Colored and Styled Hello World

# Text formatting codes
BOLD='\033[1m'
BLINK='\033[5m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'  # No Color

echo -e "${BOLD}${BLINK}${RED}Hello${NC} ${BLUE}World!${NC}"
