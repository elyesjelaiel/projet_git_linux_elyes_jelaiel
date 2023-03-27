link=$(curl -s https://www.coingecko.com/en/coins/solana)
solana=$(echo "$link" | grep -Po '^\$[\d,]+\.\d{2}$' | tail -n 1)
echo " $solana" >> solana_price.txt
echo "$(date)" >> date.txt
