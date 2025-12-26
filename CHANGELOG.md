# Changelog

## [1.4.0](https://github.com/ifokeev/airbrowser-mcp/compare/v1.3.0...v1.4.0) (2025-12-26)


### Features

* **vision:** add debug info to detect_coordinates response ([ccfae7a](https://github.com/ifokeev/airbrowser-mcp/commit/ccfae7a57bef54930e8fddd816d2b5ceae5cce35))


### Bug Fixes

* **compose:** enable hot-reload with FLASK_ENV=development ([77c62e7](https://github.com/ifokeev/airbrowser-mcp/commit/77c62e7599c81a0b2060839a1ca586e8831a1b40))
* **display:** reduce default screen resolution to 1600x900 ([fa859a7](https://github.com/ifokeev/airbrowser-mcp/commit/fa859a792226c45f4d8cf37025eebf90c150f0dd))
* **launcher:** maximize window by default, position at (0,0) ([82d5d11](https://github.com/ifokeev/airbrowser-mcp/commit/82d5d1175cd0a1a2c62d45d42b77d60e795e3b52))
* **vision:** improve coordinate detection prompt for precise clicks ([a74be50](https://github.com/ifokeev/airbrowser-mcp/commit/a74be50ba7b3af6daf6641829e4d7ca5f8ce481e))
* **vision:** require image_size in coordinate transform ([adaddc8](https://github.com/ifokeev/airbrowser-mcp/commit/adaddc8978dba67531311c1d8e2807436e82dc5c))

## [1.3.0](https://github.com/ifokeev/airbrowser-mcp/compare/v1.2.4...v1.3.0) (2025-12-26)


### Features

* **api:** normalize responses to {success, message, data} format ([5c1ca3a](https://github.com/ifokeev/airbrowser-mcp/commit/5c1ca3a8d13ac1a6124028529d730ba0a3fdbed5))
* **browser-pool:** show browsers immediately with status lifecycle ([f0caca9](https://github.com/ifokeev/airbrowser-mcp/commit/f0caca92b91a9c5bcd9e59d7d839602d4e321230))
* **compose:** add NGINX_HTTPS_PORT environment variable ([d88b126](https://github.com/ifokeev/airbrowser-mcp/commit/d88b1263200ed7020a73b3fee590363647123d0f))
* **ipc:** add configurable COMMAND_TIMEOUT_DEFAULT (20s) ([a382925](https://github.com/ifokeev/airbrowser-mcp/commit/a3829254b5da9ccdf74bbb258d15934e1e5db5f2))
* **mcp:** change get_content to return visible text instead of HTML ([2b66a67](https://github.com/ifokeev/airbrowser-mcp/commit/2b66a676bb13fc557dd33d62ff638fd36b17b379))
* **mcp:** conditionally expose vision tools based on API key ([b6a0a96](https://github.com/ifokeev/airbrowser-mcp/commit/b6a0a962786a8ad2f3b54fdcba4cdef012d7fdc0))
* **nginx:** add HTTPS support with auto-generated certificates ([2403cbf](https://github.com/ifokeev/airbrowser-mcp/commit/2403cbfbcdac87e5c441fad80de029940395e43a))
* **portable:** add environment variable support via .env file ([9141b10](https://github.com/ifokeev/airbrowser-mcp/commit/9141b106e48535f4a8dfa7420604d9624ceee0d3))
* **portable:** add HTTPS port and update service URLs ([72ecad9](https://github.com/ifokeev/airbrowser-mcp/commit/72ecad9f8f058c7fcf1b064426e884086d531981))


### Bug Fixes

* **api:** add gui_press_keys_xy and pass fx/fy to detect_coordinates ([0ead28c](https://github.com/ifokeev/airbrowser-mcp/commit/0ead28c9badbd6382f28bbfbfa15d596533f34ea))
* **browser:** pass text parameter correctly for press_keys command ([a77d6da](https://github.com/ifokeev/airbrowser-mcp/commit/a77d6dadc6a6b17198edac08d8e6f3aee60d849c))
* **browser:** properly execute special keys like ENTER, TAB in press_keys ([689ae41](https://github.com/ifokeev/airbrowser-mcp/commit/689ae4152ff5af4eb2ce7279750be88073615d74))
* **commands:** improve click/type error messages for file inputs and selectors ([518bb99](https://github.com/ifokeev/airbrowser-mcp/commit/518bb99ba5ae601e3b47e8ffdfc0ece828665363))
* **commands:** remove stacktrace from error responses ([a346473](https://github.com/ifokeev/airbrowser-mcp/commit/a3464735c7966565d3b2e3d9968931db57a9a370))
* **dashboard:** sync browser list with IPC service and add loading indicator ([6427827](https://github.com/ifokeev/airbrowser-mcp/commit/6427827c04fd7ec79fa41e8720cb50a0300efa79))
* **dashboard:** update API endpoints to match new routes ([6336adf](https://github.com/ifokeev/airbrowser-mcp/commit/6336adf75424809feacf62588d808000fc2e4f15))
* **elements:** add proper selector support for XPath, ID, and name ([448c199](https://github.com/ifokeev/airbrowser-mcp/commit/448c199b467408c248a0d6aa70cd26a5c2d8c1ed))
* **ipc:** add 60s timeout for vision commands (what_is_visible, detect_coordinates) ([b936c21](https://github.com/ifokeev/airbrowser-mcp/commit/b936c213baf68e38fe7c2e7b519d044419b22a47))
* **mcp:** return screenshot URL only, not internal Docker path ([2ad9b81](https://github.com/ifokeev/airbrowser-mcp/commit/2ad9b810e532023ddc59f8669b870e99bc79e967))
* **models:** add uc field to BrowserConfig for MCP compatibility ([c9a3abd](https://github.com/ifokeev/airbrowser-mcp/commit/c9a3abd75e8884c96c686d0c2774b3e420cc9ed3))
* **nginx:** serve screenshots at /screenshots/ path on port 18080 ([ebe4786](https://github.com/ifokeev/airbrowser-mcp/commit/ebe47867d4a2391b6ab6b40252d3bad95741f0bd))
* **vision:** preserve auto left-bias for wide elements in detect_coordinates ([a5ec79c](https://github.com/ifokeev/airbrowser-mcp/commit/a5ec79c01aa9cbe90c35b411d47b7c2b2aea0719))
* **vision:** preserve auto-bias for wide elements in detect_coordinates ([337854f](https://github.com/ifokeev/airbrowser-mcp/commit/337854fab28ea473e3b9fbb4d49e390d6e94b5ff))

## [1.2.4](https://github.com/ifokeev/airbrowser-mcp/compare/v1.2.3...v1.2.4) (2025-12-24)


### Bug Fixes

* **ci:** add pages permissions to release-please workflow ([94d21e8](https://github.com/ifokeev/airbrowser-mcp/commit/94d21e8470ad089c22cdd5572eb6bc7b5ea3b8ff))
* **ci:** deploy pages directly in release workflow ([6b9571d](https://github.com/ifokeev/airbrowser-mcp/commit/6b9571d863f29688d7990bec3eaf5729a92cb74d))


### Documentation

* regenerate documentation for v1.2.3 ([6039381](https://github.com/ifokeev/airbrowser-mcp/commit/603938116c3c931de2d5224d408875f4a3e5c3d7))

## [1.2.3](https://github.com/ifokeev/airbrowser-mcp/compare/v1.2.2...v1.2.3) (2025-12-24)


### Bug Fixes

* **ci:** use PAT for docs push to trigger pages workflow ([a0f5d99](https://github.com/ifokeev/airbrowser-mcp/commit/a0f5d99e878103369927a09b0f243c6c025d1bef))


### Documentation

* regenerate documentation for v1.2.2 ([09c8b04](https://github.com/ifokeev/airbrowser-mcp/commit/09c8b041bfd03551de4d38dc6a279408757faef2))

## [1.2.2](https://github.com/ifokeev/airbrowser-mcp/compare/v1.2.1...v1.2.2) (2025-12-24)


### Bug Fixes

* **ci:** skip CI for landing and markdown changes ([348d766](https://github.com/ifokeev/airbrowser-mcp/commit/348d766346352542df518f63365701ee1a33430f))


### Documentation

* regenerate documentation for v1.2.1 [skip ci] ([aad9b45](https://github.com/ifokeev/airbrowser-mcp/commit/aad9b456ecac2504a825fd76937066be2504ab95))

## [1.2.1](https://github.com/ifokeev/airbrowser-mcp/compare/v1.2.0...v1.2.1) (2025-12-24)


### Bug Fixes

* use relative paths for docs links in landing page ([1b23b5f](https://github.com/ifokeev/airbrowser-mcp/commit/1b23b5fd0d61fae635f94ef6168d3d8dc5d1a3df))


### Documentation

* regenerate documentation for v1.2.0 [skip ci] ([6691fec](https://github.com/ifokeev/airbrowser-mcp/commit/6691fec6417fc9b60bddc7706a77da8bafdf09af))

## [1.2.0](https://github.com/ifokeev/airbrowser-mcp/compare/v1.1.8...v1.2.0) (2025-12-24)


### Features

* **docs:** add terminal-style MCP tools documentation ([ec97323](https://github.com/ifokeev/airbrowser-mcp/commit/ec9732375ed3e0518abc69055fd6bd1c96bdfe06))

## [1.1.8](https://github.com/ifokeev/airbrowser-mcp/compare/v1.1.7...v1.1.8) (2025-12-24)


### Bug Fixes

* **ci:** inherit secrets in workflow_call ([365425e](https://github.com/ifokeev/airbrowser-mcp/commit/365425e6373c6d052ed58a537019605c20663fa7))

## [1.1.7](https://github.com/ifokeev/airbrowser-mcp/compare/v1.1.6...v1.1.7) (2025-12-24)


### Bug Fixes

* **ci:** configure npm auth token explicitly ([1642ba0](https://github.com/ifokeev/airbrowser-mcp/commit/1642ba0e35641a76089b38e549588063058615bc))

## [1.1.6](https://github.com/ifokeev/airbrowser-mcp/compare/v1.1.5...v1.1.6) (2025-12-24)


### Documentation

* **landing:** sync quickstart with README ([2272c02](https://github.com/ifokeev/airbrowser-mcp/commit/2272c02767401f28a79290a1eb23217ca0289d93))

## [1.1.5](https://github.com/ifokeev/airbrowser-mcp/compare/v1.1.4...v1.1.5) (2025-12-24)


### Bug Fixes

* **ci:** use explicit version tags for Docker images ([644e736](https://github.com/ifokeev/airbrowser-mcp/commit/644e7369af358bdc726037ad28891935d047f4e8))

## [1.1.4](https://github.com/ifokeev/airbrowser-mcp/compare/v1.1.3...v1.1.4) (2025-12-24)


### Bug Fixes

* **docker:** add pip fallback when uv installation fails ([7d7bba5](https://github.com/ifokeev/airbrowser-mcp/commit/7d7bba59b21fb2c6c35a01b6c305f9aebd4fde02))

## [1.1.3](https://github.com/ifokeev/airbrowser-mcp/compare/v1.1.2...v1.1.3) (2025-12-24)


### Bug Fixes

* **docker:** add retry logic for uv installation ([1da2588](https://github.com/ifokeev/airbrowser-mcp/commit/1da25889c4cbb52318910da73f295b6c971d6cab))

## [1.1.2](https://github.com/ifokeev/airbrowser-mcp/compare/v1.1.1...v1.1.2) (2025-12-24)


### Bug Fixes

* **portable:** rename agent-browser.bat to airbrowser.bat ([924484e](https://github.com/ifokeev/airbrowser-mcp/commit/924484e1f50950f37ffd0bd034a087ce3ce4cd9a))

## [1.1.1](https://github.com/ifokeev/airbrowser-mcp/compare/v1.1.0...v1.1.1) (2025-12-23)


### Performance

* **tests:** optimize test speed and Docker caching ([36c95a8](https://github.com/ifokeev/airbrowser-mcp/commit/36c95a87b54b759a7f8caf224c5807068f1ca021))

## [1.1.0](https://github.com/ifokeev/airbrowser-mcp/compare/v1.0.0...v1.1.0) (2025-12-23)


### Features

* initial release of Airbrowser ([df6ce02](https://github.com/ifokeev/airbrowser-mcp/commit/df6ce029d05187d17c881676e5dbd1eb75626efe))


### Bug Fixes

* **ci:** use config files for release-please action ([db561bc](https://github.com/ifokeev/airbrowser-mcp/commit/db561bcaddb88019607755e93f68f276779e228d))

## Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
