#!/bin/bash
# hello_colors.sh - Print Hello World in color, bold and blink

RED='\033[1;31m'
BROWN='\033[0;33m'
BOLD='\033[1m'
BLINK='\033[5m'
NC='\033[0m' # No Color

echo -e "${RED}${BOLD}${BLINK}Hello World in Red and Bold!${NC}"
echo -e "${BROWN}${BOLD}Hello World in Brown and Bold!${NC}"
