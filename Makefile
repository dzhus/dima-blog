.PHONY: clean

clean:
	@rm -frv `hg status --unknown --no-status`
