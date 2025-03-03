# AFLGenParallel
## _Config-based parallel fuzzing_
AFLGenParallel is util made for one not to be bothered by deprecated fuzzer 
options or hardcoded values with easy-readable config that easy to share.

## Config format
The main thing about AFLGenParallel is json config on which parallel fuzzing command generation is based.
It contains multiple fuzzer's configs that will be translated for commands, for example with this config:
```json
{
	"fuzzers": {
		"master_fuzzer": {
			"number": 1,
			"fuzzer_settings": {
				"env_variables": ["AFL_FINAL_SYNC=1"],
				"program_name": "afl-fuzz", 
				"options": {
					"-i": "in",
					"-o": "out",
					"-V": 60,
					"-x": "fuzzer.dict",
					"-M": "master_fuzzer"
				},
				"delimeter":"--",
				"target":"./fuzzer",
				"target_args": null,
				"additional": "& pids+=($!)"
			}
		},

		"asan_fuzzer": {	
			"number": 1,
			"fuzzer_settings": {
				"env_variables": ["AFL_NO_UI=1","AFL_USE_ASAN=1"],
				"program_name": "afl-fuzz", 
				"options": {
					"-i": "in",
					"-o": "out",
					"-V": 60,
					"-x": "fuzzer.dict",
					"-S": "asan_fuzzer"
				},
				"delimeter": "--",
				"target": "./asan_fuzzer",
				"target_args": null,
				"additional": "> /dev/null & pids+=($!)"		
			}
		},

		"exploit_fuzzer": {	
			"number": 3,
			"fuzzer_settings": {
				"env_variables": ["AFL_NO_UI=1"],
				"program_name": "afl-fuzz", 
				"options": {
					"-i": "in",
					"-o": "out",
					"-V": 60,
					"-x": "fuzzer.dict",
					"-S": "exploit_fuzzer"
				},
				"delimeter": "--",
				"target": "./fuzzer",
				"target_args": null,
				"additional": "> /dev/null & pids+=($!)"
			}
		}
	}
}
```
AFLGenParallel will generate that:
```bash
AFL_FINAL_SYNC=1 afl-fuzz -i in -o out -V 60 -x fuzzer.dict -M master_fuzzer -- ./fuzzer & pids+=($!)
AFL_NO_UI=1 AFL_USE_ASAN=1 afl-fuzz -i in -o out -V 60 -x fuzzer.dict -S asan_fuzzer -- ./asan_fuzzer > /dev/null & pids+=($!)
AFL_NO_UI=1 afl-fuzz -i in -o out -V 60 -x fuzzer.dict -S exploit_fuzzer -- ./fuzzer > /dev/null & pids+=($!)
AFL_NO_UI=1 afl-fuzz -i in -o out -V 60 -x fuzzer.dict -S exploit_fuzzer1 -- ./fuzzer > /dev/null & pids+=($!)
AFL_NO_UI=1 afl-fuzz -i in -o out -V 60 -x fuzzer.dict -S exploit_fuzzer2 -- ./fuzzer > /dev/null & pids+=($!)
```
For now AFLGenParallel doesn't check if certain option exists (except for "-M" and "-S") but it checks field existence and datatype.
We`re looking forward to make it more intelligent about config but not restrictive.

## Usage
```bash
usage: main.py [-h] -f CONFIG_FILE [-o OUTPUT_FILE]

options:
  -h, --help            show this help message and exit
  -f CONFIG_FILE, --config-file CONFIG_FILE
                        Config json file
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        File with AFLGenParallel output
```



