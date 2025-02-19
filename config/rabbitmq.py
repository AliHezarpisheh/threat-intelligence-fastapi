"""Module holding RabbitMQ management components."""

from typing import Any

from aio_pika import ExchangeType, connect_robust
from aio_pika.abc import (
    AbstractChannel,
    AbstractConnection,
    AbstractExchange,
    AbstractQueue,
)


class AsyncRabbitmqManager:
    """
    Async RabbitMQ manager class.

    This class provides utility methods for working with RabbitMQ in an asynchronous
    context. It facilitates the creation of connections, channels, exchanges, queues,
    and binding queues to exchanges, following RabbitMQ best practices.

    Proper lifecycle management is crucial when using this class. Connections must be
    opened and closed appropriately to avoid resource leaks. The example below
    demonstrates how to use the `AsyncRabbitmqManager` to consume messages
    while managing the connection lifecycle.

    Example
    -------
    ```python
    import asyncio
    from aio_pika.abc import AbstractIncomingMessage
    from aio_pika import ExchangeType

    async def process_message(message: AbstractIncomingMessage) -> None:
        async with message.process():
            print(f"Received: {message.body.decode()}")

    async def main():
        manager = AsyncRabbitmqManager("amqp://guest:guest@localhost/")

        # Manage connection lifecycle
        async with await manager.get_connection() as connection:
            channel = await manager.get_channel(connection)
            await channel.set_qos(prefetch_count=1)

            # Declare exchange and queue
            exchange = await manager.declare_exchange(
                channel=channel,
                name="my_exchange",
                exchange_type=ExchangeType.DIRECT,
            )

            queue = await manager.declare_queue(
                channel=channel,
                name="my_queue",
            )

            # Bind queue to exchange
            await manager.bind(exchange=exchange, queue=queue, routing_key="test")

            print("Waiting for messages...")
            # Start consuming messages
            await queue.consume(process_message)
            await asyncio.Future()  # Keep the program running

    if __name__ == "__main__":
        asyncio.run(main())
    ```
    """

    def __init__(self, amqp_url: str) -> None:
        """Initialize an `AsyncRabbitmqManager` object."""
        self._amqp_url = amqp_url

    async def get_connection(self) -> AbstractConnection:
        """
        Get a connection to RabbitMQ.

        Establishes and returns a robust connection to RabbitMQ, connecting to
        the URL provided during initialization.

        Returns
        -------
        AbstractConnection
            The connection to the RabbitMQ server.
        """
        return await connect_robust(url=self._amqp_url)

    @staticmethod
    async def get_channel(
        connection: AbstractConnection,
    ) -> AbstractChannel:
        """
        Get a channel from the RabbitMQ connection.

        Establishes a channel from the given connection. The channel should be used for
        performing RabbitMQ operations.

        Parameters
        ----------
        connection : AbstractConnection
            The connection object, used to create a channel.

        Returns
        -------
        AbstractChannel
            The channel for interacting with RabbitMQ.
        """
        channel = await connection.channel()
        return channel

    @staticmethod
    async def declare_exchange(
        *,
        channel: AbstractChannel,
        name: str,
        exchange_type: ExchangeType = ExchangeType.DIRECT,
        durable: bool = True,
        auto_delete: bool = False,
        arguments: dict[str, Any] | None = None,
    ) -> AbstractExchange:
        """
        Declare an exchange on RabbitMQ.

        Declares an exchange with the specified parameters on the RabbitMQ server.

        Parameters
        ----------
        channel : AbstractChannel
            The channel connected to RabbitMQ used to declare the exchange.
        name : str
            The name of the exchange to declare.
        exchange_type : ExchangeType, optional
            The type of the exchange (default is `ExchangeType.DIRECT`).
        durable : bool, optional
            Whether the exchange should survive server restarts (default is True).
        auto_delete : bool, optional
            Whether the exchange should be deleted when no consumers are connected
            (default is False).
        arguments: dict[str, Any], optional
            The arguments for the exchange (default is None).

        Returns
        -------
        AbstractExchange
            The declared exchange.
        """
        exchange = await channel.declare_exchange(
            name=name,
            type=exchange_type,
            durable=durable,
            auto_delete=auto_delete,
            arguments=arguments,
        )
        return exchange

    @staticmethod
    async def declare_queue(
        *,
        channel: AbstractChannel,
        name: str | None = None,
        durable: bool = True,
        auto_delete: bool = False,
        exclusive: bool = False,
        arguments: dict[str, Any] | None = None,
    ) -> AbstractQueue:
        """
        Declare a queue on RabbitMQ.

        Declares a queue with the specified parameters on the RabbitMQ server.

        Parameters
        ----------
        channel : AbstractChannel
            The channel connected to RabbitMQ used to declare the exchange.
        name : str, optional
            The name of the queue to declare. If the name set to None, the server will
            generate a random name for the queue. (default is None)
        durable : bool, optional
            Whether the queue should survive server restarts (default is True).
        auto_delete : bool, optional
            Whether the queue should be deleted when no consumers are connected
            (default is False).
        exclusive: bool, optional
            Wether the queues should exclusive to the created connection or not.
            (default is False)
        arguments: dict[str, Any], optional
            The arguments for the exchange (default is None).

        Returns
        -------
        AbstractQueue
            The declared queue.
        """
        queue = await channel.declare_queue(
            name=name,
            durable=durable,
            auto_delete=auto_delete,
            exclusive=exclusive,
            arguments=arguments,
        )
        return queue

    @staticmethod
    async def bind(
        *,
        exchange: AbstractExchange,
        queue: AbstractQueue,
        routing_key: str = "",
    ) -> None:
        """
        Bind a queue to an exchange.

        Binds a queue to an exchange with an optional routing key.

        Parameters
        ----------
        exchange : AbstractExchange
            The exchange to bind the queue to.
        queue : AbstractQueue
            The queue to bind.
        routing_key : str, optional
            The routing key to use for binding (default is an empty string).
        """
        await queue.bind(exchange=exchange, routing_key=routing_key)

    @staticmethod
    async def set_qos(
        *, channel: AbstractChannel, prefetch_count: int, prefetch_size: int = 0
    ) -> None:
        """
        Set QoS settings for the channel.

        Configures the number of messages or the maximum message size to be sent to a
        consumer before an acknowledgment is required.

        Parameters
        ----------
        channel : AbstractChannel
            The channel to configure.
        prefetch_count : int
            The number of messages to send before waiting for an acknowledgment.
        prefetch_size : int, optional
            The maximum size (in bytes) of messages to send. Default is 0 (unlimited).
        """
        await channel.set_qos(
            prefetch_count=prefetch_count, prefetch_size=prefetch_size
        )
