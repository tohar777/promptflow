# Prompt flow
![banner](examples/tutorials/quick-start/media/PF_banner.png)

[![Python package](https://img.shields.io/pypi/v/promptflow)](https://pypi.org/project/promptflow/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/promptflow)](https://pypi.org/project/promptflow/)
[![License: MIT](https://img.shields.io/github/license/microsoft/promptflow)](https://github.com/microsoft/promptflow/blob/main/LICENSE)

> Welcome to join us to make Prompt flow!

[Documentacion](https://microsoft.github.io/promptflow) • [Quick Start](https://github.com/microsoft/promptflow/blob/main/docs/how-to-guides/quick-start.md)  • [Discord](https://discord.gg/bnXr6kxs) •  [Discussions](https://github.com/microsoft/promptflow/discussions) • [Issues](https://github.com/microsoft/promptflow/issues/new/choose) • [Contribute PRs](https://github.com/microsoft/promptflow/pulls).

**Prompt flow** is a suite of development tools designed to streamline the end-to-end development cycle of LLM-based AI applications, from ideation, prototyping, testing, evaluation to production deployment and monitoring. It makes prompt engineering much easier and enables you to build LLM apps with production quality.

With prompt flow, you will be able to:

- **Create and Iteratively Develop Flow**
    - Create executable workflows that link LLMs, prompts, Python code and other tools together.
    - Debug and iterate your flows, especially the interaction with LLMs with ease.
- **Evaluate Flow Quality and Performance**
    - Evaluate your flow's quality and performance with larger datasets.
    - Integrate the testing and evaluation into your CI/CD system to ensure quality of your flow.
    - Deploy your flow to the serving platform you choose or integrate into your app's code base easily.
- (Optional but highly recommended) Collaborate with your team by leveraging the cloud version of [Prompt flow in Azure AI](https://learn.microsoft.com/en-us/azure/machine-learning/prompt-flow/overview-what-is-prompt-flow?view=azureml-api-2).

### Concept Overview

![concept](examples/tutorials/quick-start/media/concept.png)
Learn more about the concept of Prompt flow [here](https://microsoft.github.io/promptflow/concepts/index.html).

------

## Installation
> ℹ️ A python environment, `python=3.9` is recommended.

```sh
pip install promptflow promptflow-tools
```

## Quick Start ⚡

This section will guide you quick start with Prompt flow from creating a simple chat flow from template.

### Initialize a prompt flow using the chat template

<details>
<summary>Click to toggle the detailed introduction of the command</summary>

Use the following CLI command to initiate a prompt flow from a chat template. This will create a new **flow folder** named "my_chatbot" and initiate flow files within it.

You can find a flow.dag.yaml file which is the flow definition with inputs/outputs, nodes, tools and variants for authoring purpose.

> The `--flow` argument is used to specify the path to the flow folder.
</details>

```sh
pf flow init --flow ./my_chatbot --type chat
```

### Setup a connection for your API key

Navigate to the `my_chatbot` folder, you can find a `openai.yaml` file, which is the connection configuration file.
<details>
<summary>Click to toggle the yaml.</summary>

```yaml
$schema: https://azuremlschemas.azureedge.net/promptflow/latest/OpenAIConnection.schema.json
name: open_ai_connection # name of the connection
type: open_ai # Open AI 
api_key: "<user-input>" # replace with your OpenAI API key
```
</details>

Establish the connection by running:
```sh
# Override keys with --set to avoid yaml file changes
pf connection create --file openai.yaml --set api_key=<your_api_key>
```

<details>
<summary>For <a herf="https://azure.microsoft.com/en-us/products/ai-services/openai-service-b">Azure Open AI</a>, click to toggle the setup.</summary>

Create a new yaml file `azure_openai.yaml` in the `my_chatbot` folder. Replace the `api_key` and `api_base` with your own Azure OpenAI API key and endpoint:

```yaml
$schema: https://azuremlschemas.azureedge.net/promptflow/latest/AzureOpenAIConnection.schema.json
name: azure_open_ai_connection # name of the connection
type: azure_open_ai  # Azure Open AI 
api_key: "<aoai-api-key>" # replace with your Azure OpenAI API key
api_base: "aoai-api-endpoint" # replace with your Azure OpenAI API endpoint
api_type: "azure" 
api_version: "2023-03-15-preview" # replace with your Azure OpenAI API version
```

Establish the connection by running:
```sh
pf connection create --file azure_openai.yaml
```
</details>

### Chat with your flow

Note in `flow.dag.yaml` we are using connection named `open_ai_connection`.

<details>
<summary>For Azure Open AI, click to toggle the modification</summary>
Navigate to the `my_chatbot` folder, you can find a `flow.dag.yaml` file, which is the definition of the flow, including the inputs/outputs, tools, nodes, connection of llm node, etc.

For Azure Open AI, please replace it with the connection name you created in the previous step.

```yaml
nodes:
- name: chat
  type: llm
  source:
    type: code
    path: chat.jinja2
  inputs:
    deployment_name: gpt-4
    max_tokens: '256'
    temperature: '0.7'
    chat_history: ${inputs.chat_history}
    question: ${inputs.question}
  api: chat
  connection: azure_open_ai_connection
```

</details>
Interact with it by running (press "Ctrl + C" to end the session):

```sh
pf flow test --flow ./my_chatbot --interactive
```

### What's Next? Improve Your Chatbot on a specific task

Ensuring "High Quality” of your chat bot with Prompt Flow.

<details>
<summary><b> Before deploying your application to production, it is crucial to evaluate its quality. </b> Click to toggle why is it so important?</summary>

LLMs' randomness can yield unstable answers. Fine-tuning prompts can improve output reliability.  For accurate quality assessment, it's essential to test with larger datasets and compare outcomes with the ground truth.

During fine-tuning the prompt, we also consider to strike a balance between the accuracy and the token cost of the LLM.

Invest just 15 minutes to understand how prompt flow accelerates prompt tuning, testing, and evaluation, to find an ideal prompt **(accuracy ↑,token ↓)**
<img src="examples/tutorials/quick-start/media/realcase.png" alt="comparison resutl" width=80%>
</details>

Try the [15-mins Easy Case](examples/tutorials/quick-start/promptflow-quality-improvement.md) on Tuning ➕ Batch Testing ➕ Evaluation ➡ Quality ready for production.

Next Step! Continue with the **Tutorial**  👇 section to delve deeper into Prompt flow.

## Tutorial 🏃‍♂️

Prompt Flow is a tool designed to **facilitate high quality LLM-native apps to production**, the development process in prompt flow follows these steps: Develop a flow， improve the flow quality, deploy the flow to production.

### Develop your own LLM apps

Begin with our comprehensive [Step-by-Step Guide](https://microsoft.github.io/promptflow/how-to-guides/quick-start.html): This is a detailed walkthrough step-by-step to create your own flow from scratch and invoke your first flow run.

#### VS Code Extension

In addition to the SDK, we offer a <img src="examples/tutorials/quick-start/media/logo_pf.png" alt="alt text" width="25"/>**Prompt flow VS Code extension** for an interactive and user-friendly flow development experience. Install it from [visualstudio marketplace](https://marketplace.visualstudio.com/items?itemName=prompt-flow.prompt-flow).

<details>
<summary> <b>Demo</b> (click to toggle the content)</summary>
This is a detailed walkthrough step-by-step to create your own flow from scratch and invoke your first flow run.

[![vsc extension](https://img.youtube.com/vi/GmhasXd7sj4/0.jpg)](https://youtu.be/GmhasXd7sj4)

</details>

### Learn from Use Cases

Go through the tutorial of a practical use case, [Chat with PDF](https://github.com/microsoft/promptflow/blob/main/examples/tutorials/e2e-development/chat-with-pdf.md): This is an end-to-end tutorial on how to build a high quality chat application with prompt flow, including flow development and evaluation with metrics.
* You can find more examples [here](./examples/README.md). We always welcome contributions of new use cases!

### Setup for Contributors

Contribute to Prompt flow, please start with our dev setup guide: [dev_setup.md](./docs/dev/dev_setup.md).

Next Step! Continue with the **Contributing**  👇 section to to contribute to Prompt flow.

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft
trademarks or logos is subject to and must follow
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.

## Code of Conduct

This project has adopted the
[Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the
[Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/)
or contact [opencode@microsoft.com](mailto:opencode@microsoft.com)
with any additional questions or comments.

## License

Copyright (c) Microsoft Corporation. All rights reserved.

Licensed under the [MIT](LICENSE) license.
