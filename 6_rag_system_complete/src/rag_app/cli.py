
"""Command-line interface for theRAG application."""

import argparse
import logging
import os
from pathlib import Path

from rag_app.config import Settings
from rag_app.logging_config import config_logging
from rag_app.pipeline import RAGApplication

# TODO