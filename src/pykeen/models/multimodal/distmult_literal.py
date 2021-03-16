# -*- coding: utf-8 -*-

"""Implementation of the DistMultLiteral model."""

from typing import Any, ClassVar, Mapping, Optional

import torch.nn as nn

from .base import LiteralModel
from .combinations import DistMultCombination
from ...constants import DEFAULT_DROPOUT_HPO_RANGE, DEFAULT_EMBEDDING_HPO_EMBEDDING_DIM_RANGE
from ...losses import Loss
from ...nn import Embedding
from ...regularizers import Regularizer
from ...nn import EmbeddingSpecification
from ...nn.modules import DistMultInteraction, LiteralInteraction
from ...triples import TriplesNumericLiteralsFactory
from ...typing import DeviceHint

__all__ = [
    'DistMultLiteral',
]


class DistMultLiteral(LiteralModel):
    """An implementation of the LiteralE model with the DistMult interaction from [kristiadi2018]_.

    ---
    citation:
        author: Kristiadi
        year: 2018
        link: https://arxiv.org/abs/1802.00934
    """

    #: The default strategy for optimizing the model's hyper-parameters
    hpo_default: ClassVar[Mapping[str, Any]] = dict(
        embedding_dim=DEFAULT_EMBEDDING_HPO_EMBEDDING_DIM_RANGE,
        input_dropout=DEFAULT_DROPOUT_HPO_RANGE,
    )
    #: The default parameters for the default loss function class
    loss_default_kwargs: ClassVar[Mapping[str, Any]] = dict(margin=0.0)

    def __init__(
        self,
        triples_factory: TriplesNumericLiteralsFactory,
        embedding_dim: int = 50,
        input_dropout: float = 0.0,
        loss: Optional[Loss] = None,
        preferred_device: DeviceHint = None,
        random_seed: Optional[int] = None,
        regularizer: Optional[Regularizer] = None,
        predict_with_sigmoid: bool = False,
    ) -> None:
        super().__init__(
            triples_factory=triples_factory,
            interaction=LiteralInteraction(
                base=DistMultInteraction(),
                combination=DistMultCombination(
                    embedding_dim=embedding_dim,
                    num_of_literals=triples_factory.numeric_literals.shape[1],
                    input_dropout=input_dropout,
                ),
            ),
            entity_representations=[
                EmbeddingSpecification(
                    embedding_dim=embedding_dim,
                    initializer=nn.init.xavier_normal_,
                    # TODO: Verify
                    regularizer=regularizer,
                ),
            ],
            relation_representations=[
                EmbeddingSpecification(
                    embedding_dim=embedding_dim,
                    initializer=nn.init.xavier_normal_,
                    # TODO: Verify
                    regularizer=regularizer,
                ),
            ],
            loss=loss,
            predict_with_sigmoid=predict_with_sigmoid,
            preferred_device=preferred_device,
            random_seed=random_seed,
        )
