"""
Test file for the device client. Depends on d3a test setup file strategy_tests.external_devices
"""
from time import sleep
from d3a_api_client.redis_device import RedisDeviceClient


class AutoOfferBidOnMarket(RedisDeviceClient):

    def on_market_cycle(self, market_info):
        """
        Places a bid or an offer whenever a new market is created. The amount of energy
        for the bid/offer depends on the available energy of the PV, or on the required
        energy of the load.
        :param market_info: Incoming message containing the newly-created market info
        :return: None
        """
        print(f"New market information {market_info}")
        if "available_energy_kWh" in market_info and market_info["available_energy_kWh"] > 0.0:
            offer = self.offer_energy(market_info["available_energy_kWh"], 0.1)
            print(f"Offer placed on the new market: {offer}")
        print(market_info["energy_requirement_kWh"])
        if market_info["energy_requirement_kWh"] > 0.0:
            bid = self.bid_energy(market_info["energy_requirement_kWh"], 100)
            print(f"Bid placed on the new market: {bid}")
        print(f"Aggregated device/market statistics: {self.list_stats()}")


# Connects one client to the load device
load = AutoOfferBidOnMarket('load', autoregister=True)
# Connects a second client to the pv device
pv = AutoOfferBidOnMarket('pv', autoregister=True)


# Infinite loop in order to leave the client running on the background
# placing bids and offers on every market cycle.
while True:
    sleep(0.5)
