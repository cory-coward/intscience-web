from pylogix import PLC
from pylogix.eip import Response
from typing import List, Tuple, Union

PlcResponse = Union[List[Response], Response]


class PlcCore:
    def __init__(self, ip_address: str):
        self.ip_address = ip_address

    def read_tag(self, tag_name: str, num_elements: Union[int, None]) -> PlcResponse:
        with PLC(self.ip_address) as comm:
            if num_elements is None:
                response = comm.Read(tag_name)
            else:
                response = comm.Read(tag_name, num_elements)
            return response

    def read_list_of_tags(self, list_to_read: List[str]) -> PlcResponse:
        with PLC(self.ip_address) as comm:
            response = comm.Read(list_to_read)
            return response

    def write_tag(self, tag_name: str, val: any) -> PlcResponse:
        with PLC(self.ip_address) as comm:
            response = comm.Write(tag_name, val)
            return response

    def write_tag_list(self, data: List[Tuple[str, any]]) -> PlcResponse:
        with PLC(self.ip_address) as comm:
            response = comm.Write(data)
            return response
