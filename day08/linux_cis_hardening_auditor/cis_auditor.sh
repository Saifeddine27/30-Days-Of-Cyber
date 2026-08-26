#!/bin/bash

TOTAL=0
PASSED=0
FAILED=0

run_check() {

    local id="$1"
    local name="$2"
    local cmd="$3"
    local expected="$4"
    local remedy="$5"

    ((TOTAL++))

    echo "[*] Checking CIS $id: $name..."

    local output=$(eval "$cmd" 2>/dev/null)

    if [[ "$output" == *"$expected"* ]]; then
        echo -e "    [+] Status: SECURE (Pass)"
        ((PASSED++))
    else
        echo -e "    [-] Status: VULNERABLE (Fail)"
        echo -e "    [!] Found: '$output'"
        echo -e "    [>] Remedy: $remedy"
        ((FAILED++))
    fi
    echo "" 
}


echo "Démarrage de l'audit système CIS..."
echo "========================================="

# Test 1 : Vérifier que le pare-feu UFW est actif
run_check "3.5.1" \
          "Ensure Uncomplicated Firewall (UFW) is active" \
          "LC_ALL=C ufw status" \
          "active" \
          "Run 'sudo apt install ufw' and 'sudo ufw enable'"

# Test 2 : Vérifier que le compte Root ne peut pas se connecter à distance (SSH)
run_check "5.2.8" \
          "Ensure SSH root login is disabled" \
          "grep '^PermitRootLogin' /etc/ssh/sshd_config" \
          "PermitRootLogin no" \
          "Edit /etc/ssh/sshd_config, set 'PermitRootLogin no', and run 'sudo systemctl restart sshd'"

# Test 3 : Vérifier les permissions du fichier des mots de passe (/etc/shadow)
run_check "6.1.3" \
          "Ensure permissions on /etc/shadow are configured" \
          "stat -c %a /etc/shadow" \
          "640" \
          "Run 'sudo chmod 640 /etc/shadow'"


echo ""
echo "========================================="
echo "             AUDIT REPORT                "
echo "========================================="
echo "  Total Checks : $TOTAL"
echo "  Passed       : $PASSED"
echo "  Failed       : $FAILED"

if [ $TOTAL -gt 0 ]; then
    SCORE=$(( (PASSED * 100) / TOTAL ))
    echo "  Security Score: $SCORE%"
else
    echo "  Security Score: 0%"
fi
echo "========================================="

if [ $FAILED -gt 0 ]; then
    echo -e "\n[!] ACTION REQUIRED: You have $FAILED vulnerable configurations."
    echo "    Please review the 'Remedy' steps above to harden your system."
else
    echo -e "\n[+] PERFECT! System is fully hardened according to current checks."
fi