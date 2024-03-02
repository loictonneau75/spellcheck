# SpellCheck

## Introduction

SpellCheck is a Python library designed to check and correct spelling errors in texts across multiple languages using OpenAI's large language models (LLMs). It leverages the `langchain_openai.ChatOpenAI` interface to offer a seamless integration for developers looking to enhance their applications with advanced spell checking capabilities.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Dependencies](#dependencies)
- [Configuration](#configuration)
- [Documentation](#documentation)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [License](#license)
- [Future](#Future)

## Installation
To install SpellCheck, run the following command:
```bash
pip install git+https://github.com/loictonneau75/spellcheck.git
```
## Usage

Here's a simple example to get you started:

```python
from spellcheck.spellcheck import SpellCheck


open_api_key = "your_open_api_key"
SpellCheck = sp(open_api_key,"eng")
print(sp("This is a smaple sentence with a spleling error."))
```
## Feature
- Multi-language support
- Integration with OpenAI's LLMs
- Customizable correction thresholds

## Dependencies
SpellCheck requires the following:

- Python 3.6+
- langchain_openai library
- langchain_core library
- OpenAI API key

See the [REQUIREMENTS](requirements.txt) file for more details.

## Configuration

You need to first get an OpenAI API key here : [OpenAI API](https://platform.openai.com/api-keysm)

## Documentation

Refer to the code comments for detailed documentation on each method and class usage.

## Example

See the [Usage](#usage) section for a simple example. More examples can be added here as needed.

## License

SpellCheck is released under the MIT License. See the [LICENSE](LICENSE.txt) file for more details.

## Contribution

Be free to contribute and open prs or issues to improve the code !

If you want more infos on repos please open an issue !

## Future

Better managing whitespace
