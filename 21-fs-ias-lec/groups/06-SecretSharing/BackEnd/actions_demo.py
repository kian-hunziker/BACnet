
from os import urandom
import BackEnd.actions as act


if __name__ == '__main__':

    print("Test Actions")

    secret = urandom(16)
    print(secret)
    packages, sinfo = act.split_secret_into_share_packages("MySecret", secret, 5)
    print(sinfo)
    act.push_packages_into_share_buffer(packages, sinfo)

    act.set_password("Qwe123??")

    act.save_state()

    act.encrypt_state("Qwe123??")
    
    act.decrypt_state("Qwe123??")

    #
    # mock_secret = urandom(58)
    # packages = act.split_large_secret_into_share_packages(0, mock_secret, 5)
    # mock_secret_reconstructed = act.recover_large_secret(packages)
    #
    # print("original secret")
    # print(mock_secret)
    # print("secret reconstructed")
    # print(mock_secret_reconstructed)

    # # splitting shares, encoding to strings
    #
    # mock_secret_true = urandom(16)
    # print("test")
    # print(mock_secret_true)
    #
    # act.secret_to_buffered_shares(mock_secret_true, "mock_secret", 5, 5)
    #
    # # reconstructing secret from share packages
    #
    # mock_secret_reconstructed = act.resolve_packages_to_secret("mock_secret")
    #
    # print("test resolution")
    # print("true: " + str(mock_secret_true))
    # print("reco: " + str(mock_secret_reconstructed))
    #
    # # receiving shares from peer:
    #
    # mock_share_package = bytes(
    #     bytearray.fromhex('00') + bytearray.fromhex('02') + bytearray.fromhex('00') + bytearray(urandom(16))
    # ).decode('ISO-8859-1')
    # mock_contact_id = "Victor"
    #
    # act.receive_contact_share(mock_contact_id, mock_share_package)
    #
    # # receiving BACK shares:
    #
    # mock_share_package0 = bytes(
    #     bytearray.fromhex('02') + bytearray.fromhex('03') + bytearray.fromhex('00') + bytearray(urandom(16))
    # ).decode('ISO-8859-1')
    # mock_share_package1 = bytes(
    #     bytearray.fromhex('02') + bytearray.fromhex('03') + bytearray.fromhex('01') + bytearray(urandom(16))
    # ).decode('ISO-8859-1')
    # mock_share_package2 = bytes(
    #     bytearray.fromhex('02') + bytearray.fromhex('03') + bytearray.fromhex('02') + bytearray(urandom(16))
    # ).decode('ISO-8859-1')
    #
    # act.insert_mapping("forgotten_mock_secret", "2")  # normally we already have the mapping so ignore
    #
    # act.receive_returned_share(mock_share_package2)
    # act.receive_returned_share(mock_share_package0)
    # act.receive_returned_share(mock_share_package1)