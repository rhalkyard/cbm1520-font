ROM := source/325340-03.bin
OUTPUTFILES := cbm1520.bin cbm1520.jhf cbm1520.json

all: $(OUTPUTFILES)

clean:
	rm -f $(OUTPUTFILES)

cbm1520.jhf: cbm1520.json
	python3 scripts/json2hershey.py --header $< $@

cbm1520.json: $(ROM)
	python3 scripts/extract1520.py $< $@

cbm1520.bin: $(ROM)
	dd if=$< of=$@ bs=1 skip=1 count=660
