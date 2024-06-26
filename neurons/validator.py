# The MIT License (MIT)
# Copyright © 2023 Yuma Rao
# Copyright © 2024 Vector Chat

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.


import time

# Bittensor
import bittensor as bt

# Bittensor Validator Template:
import chunking
from chunking.validator import forward

# import base validator class which takes care of most of the boilerplate
from chunking.base.validator import BaseValidatorNeuron
import os
from openai import OpenAI

class Validator(BaseValidatorNeuron):
    """
    Your validator neuron class. You should use this class to define your validator's behavior. In particular, you should replace the forward function with your own logic.

    This class inherits from the BaseValidatorNeuron class, which in turn inherits from BaseNeuron. The BaseNeuron class takes care of routine tasks such as setting up wallet, subtensor, metagraph, logging directory, parsing config, etc. You can override any of the methods in BaseNeuron if you need to customize the behavior.

    This class provides reasonable default behavior for a validator such as keeping a moving average of the scores of the miners and using them to set weights at the end of each epoch. Additionally, the scores are reset for new hotkeys at the end of each epoch.
    """

    def __init__(self, config=None):
        super(Validator, self).__init__(config=config)
        
        bt.logging.info("load_state()")
        self.load_state()
        if not config.openaikey:
            print("Must provide OpenAI API key with --openaikey <OPENAIKEY>")
        os.environ["OPENAI_API_KEY"] = config.openaikey
        self.client = OpenAI()
        self.numEmbeddings = 10
        # TODO(developer): Anything specific to your use case you can do here

    async def forward(self, synapse: chunking.protocol.chunkSynapse=None):
        """
        Validator forward pass. Consists of:
        - Generating the query
        - Querying the miners
        - Getting the responses
        - Rewarding the miners
        - Updating the scores
        """

        return await forward(self, synapse)

#    async def blacklist(self, synapse: chunking.protocol.chunkSynapse) -> Tuple[bool, str]:
            # TODO add hotkeys to blacklist her as needed
            # blacklist the hotkeys mining on the subnet to prevent any potential issues
            #hotkeys_to_blacklist = [h for i,h in enumerate(self.hotkeys) if self.metagraph.S[i] < 20000 and h != self.wallet.hotkey.ss58_address]
            #if synapse.dendrite.hotkey in hotkeys_to_blacklist:
            #    return True, "Blacklisted hotkey - miners can't connect, use a diff hotkey."
#            return False, ""

    async def priority(self, synapse: chunking.protocol.chunkSynapse) -> float:
        # high priority for organic traffic
        return 1000000.0
        
# The main function parses the configuration and runs the validator.
if __name__ == "__main__":
    with Validator() as validator:
        while True:
            bt.logging.info("Validator running...", time.time())
            time.sleep(5)
