"""Module handles the publishing of new threat_report messages to RabbitMQ exchange."""

from aio_pika import DeliveryMode, ExchangeType, Message
from aio_pika.abc import AbstractChannel, AbstractExchange

from app.threat.models import ThreatReport
from config.base import logger
from config.rabbitmq import AsyncRabbitmqManager

THREAT_REPORT_EXCHANGE_NAME = "threat_report_exchange"


class ThreatReportProducer:
    """Produce and publish new threat report messages to a RabbitMQ exchange."""

    def __init__(self, rabbitmq_manager: AsyncRabbitmqManager) -> None:
        """Instantiate a `ThreatReportProducer` object."""
        self.rabbitmq_manager = rabbitmq_manager

    async def produce_new_threat_report(self, threat_report: ThreatReport) -> None:
        """
        Publish a threat message to a RabbitMQ exchange.

        Parameters
        ----------
        threat_report : ThreatReport
            The threat report object to be serialized and published.
        """
        async with await self.rabbitmq_manager.get_connection() as connection:
            logger.info("Opening connection and channel to publish thread report...")
            channel = await self.rabbitmq_manager.get_channel(connection=connection)

            threat_report_exchange = await self.declare_threat_report_exchange(
                channel=channel
            )

            message = Message(
                body=threat_report.to_bytes(),
                delivery_mode=DeliveryMode.PERSISTENT,
            )
            publish_result = await threat_report_exchange.publish(
                message=message, routing_key=self._get_new_threat_report_routing_key()
            )
            logger.info(
                "Published threat report to the %s exchange with the result: %s",
                THREAT_REPORT_EXCHANGE_NAME,
                publish_result,
            )

    async def declare_threat_report_exchange(
        self, channel: AbstractChannel
    ) -> AbstractExchange:
        """
        Declare the 'threat_reports' exchange on the specified channel.

        Parameters
        ----------
        channel : AbstractChannel
            The channel on which to declare the exchange.

        Returns
        -------
        AbstractExchange
            The declared exchange object.
        """
        threat_report_exchange = await self.rabbitmq_manager.declare_exchange(
            channel=channel,
            name=THREAT_REPORT_EXCHANGE_NAME,
            exchange_type=ExchangeType.DIRECT,
        )
        return threat_report_exchange

    @staticmethod
    def _get_new_threat_report_routing_key() -> str:
        """
        Retrieve the routing key for new threat_report messages.

        Returns
        -------
        str
            The routing key for new threat reports, typically 'threat_reports.new'.
        """
        return "threat_report.new"
