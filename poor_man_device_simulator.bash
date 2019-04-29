redis-cli PUBLISH sinewave "{\"timestamp\": `date +%s`, \"values\": [$RANDOM, $RANDOM, $RANDOM]}"
