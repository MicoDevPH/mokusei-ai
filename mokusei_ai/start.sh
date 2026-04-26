#!/bin/bash

# --- Jupiter High-Fidelity Palette ---
J_CLOUD='\033[38;5;231m'   # Ammonia White
J_ZONE='\033[38;5;223m'    # Sandy Zone
J_BELT='\033[38;5;137m'    # Brownish Belt
J_STORM='\033[38;5;130m'   # Deep Rust
J_SPOT='\033[38;5;160m'    # Great Red Spot
CYAN='\033[38;5;51m'
BOLD='\033[1m'
NC='\033[0m'

# --- 1. Enhanced Jovian Boot Sequence ---
clear
echo -e "${J_ZONE}[ SCAN ]${NC} Piercing the Ammonia Clouds..."
sleep 0.3
echo -e "${J_BELT}[ DATA ]${NC} Analyzing Zonal Jet Streams (335 mph)..."
sleep 0.4
echo -e "${J_SPOT}[ WARN ]${NC} Entering the Great Red Spot..."

for i in {1..100}; do 
    echo -ne "${J_SPOT}🌀 SPINNING STORM... ${i}% ${NC}\r"
    sleep 0.01
done
echo -e "\n${J_CLOUD}[ OK ]${NC} Planetary core reached. Stability: 100%"
sleep 0.5

# --- 2. The Jupiter Masterpiece ---
clear
echo -e "${BOLD}"
echo -e "${J_CLOUD}  ███╗   ███╗ ██████╗ ██╗  ██╗██╗   ██╗███████╗███████╗██╗"
echo -e "${J_ZONE}  ████╗ ████║██╔═══██╗██║ ██╔╝██║   ██║██╔════╝██╔════╝██║"
echo -e "${J_BELT}  ██╔████╔██║██║   ██║█████╔╝ ██║   ██║███████╗█████╗  ██║"
echo -e "${J_STORM}  ██║╚██╔╝██║██║   ██║██╔═██╗ ██║   ██║╚════██║██╔══╝  ██║"
echo -e "${J_SPOT}  ██║ ╚═╝ ██║╚██████╔╝██║  ██╗╚██████╔╝███████║███████╗██║"
echo -e "${J_SPOT}  ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝╚═╝"
echo -e "               ${J_CLOUD}🪐 ${BOLD}M O K U S E I   A I ${NC}${J_CLOUD}🪐${NC}"
echo -e "               ${J_STORM}${BOLD}───── By: ${J_CLOUD}MicoDevPH ${J_STORM}─────${NC}"
echo -e "${J_STORM}  ──────────────────────────────────────────────────────────${NC}"

# --- 3. Planetary Metrics ---
echo -e "${CYAN}[1/2]${NC} 🛰️  Checking Atmospheric Env..."
if [ -f .env ]; then
    echo -e "      ${J_CLOUD}✅ Signals Nominal (.env found)${NC}"
else
    echo -e "      ${BOLD}⚠️  Radio Silence: .env missing${NC}"
fi

echo -e "${CYAN}[2/2]${NC} ☄️  Igniting Main Engines..."
echo -e "      ${J_ZONE}Mission Control: ${BOLD}http://localhost:8000${NC}"
echo -e "      ${J_ZONE}Star Chart:      ${BOLD}https://github.com/MicoDevPH${NC}"
echo ""
echo -e "${J_BELT}--- RADIOWAVE STREAM ---${NC}"

# --- Execution ---
uvicorn mokusei_ai.main:app --host 0.0.0.0 --port 8000 --reload --no-access-log --log-level info
