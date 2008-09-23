.PHONY: clean

clean:
	@rm -frv tagging/.svn/ tagging/tests/
	@rm -frv `hg status --unknown --no-status`