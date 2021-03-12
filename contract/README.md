# Guestbook
guestbook smart contract

testnet is a global alias for *tezos-client -S -A testnet-tezos.giganode.io -P 443*

$ testnet get balance for thanos
100.128578 ꜩ

## list contracts
testnet list known contracts
guestbook: KT1NunBWtpABstxkqW7QJAfBWUbFHxn2zCXX

## compile to Michelson
~/smartpy-cli/SmartPy.sh test guestbook.py output

## originate the contract: KT18iu9dNhh1QJ1SfqfZxiFZMwYo4bUay7e2
testnet originate contract guestbook \
transferring 0 from thanos running output/Guestbook_interpreted/testContractCode.0.1.tz --force \
--fee 0.0008 --init "Pair {} (Pair {} {})" --burn-cap 0.12425 --dry-run

## get contract storage for guestbook
testnet get contract storage for guestbook

## calling the contract
testnet call guestbook from thanos \
--arg '(Pair "alice" "hi from alice")' \
--burn-cap 0.0085 --dry-run
