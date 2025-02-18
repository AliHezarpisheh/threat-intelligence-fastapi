#!/usr/bin/env bash

set -e

GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}Executing ruff...${NC}"
ruff format .

echo -e "\n${GREEN}Executing isort...${NC}"
isort .
