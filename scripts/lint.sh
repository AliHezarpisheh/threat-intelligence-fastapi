#!/usr/bin/env bash

GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}Executing ruff...${NC}"
ruff check . --fix .

echo -e "\n${GREEN}Executing mypy...${NC}"
mypy .
