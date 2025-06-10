"""Backward-compatible wrapper for RunPod client."""

from gradio_client import Client

from auth.runpod_client import RunPodClient

__all__ = ["RunPodClient", "Client"]
