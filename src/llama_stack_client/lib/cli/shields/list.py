# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.

import json
import argparse

from tabulate import tabulate

from llama_stack_client import LlamaStackClient
from llama_stack_client.lib.cli.subcommand import Subcommand


class ShieldsList(Subcommand):
    def __init__(self, subparsers: argparse._SubParsersAction):
        super().__init__()
        self.parser = subparsers.add_parser(
            "list",
            prog="llama-stack-client shields list",
            description="Show available llama models at distribution endpoint",
            formatter_class=argparse.RawTextHelpFormatter,
        )
        self._add_arguments()
        self.parser.set_defaults(func=self._run_shields_list_cmd)

    def _add_arguments(self):
        self.parser.add_argument(
            "endpoint",
            type=str,
            help="Llama Stack distribution endpoint",
        )

    def _run_shields_list_cmd(self, args: argparse.Namespace):
        client = LlamaStackClient(
            base_url=args.endpoint,
        )

        headers = [
            "Shield Type",
            "Provider ID",
            "Provider Config",
        ]

        shields_list_response = client.shields.list()
        rows = []

        for shield_spec in shields_list_response:
            rows.append(
                [
                    shield_spec.shield_type,
                    shield_spec.provider_config.provider_id,
                    json.dumps(shield_spec.provider_config.config, indent=4),
                ]
            )

        print(tabulate(rows, headers=headers, tablefmt="grid"))
