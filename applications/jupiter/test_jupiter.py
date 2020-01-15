import utils
import network
import dev_global


def unit_test_utils():
    print("test read_json")
    print(dev_global.env.CONF_FILE)
    print(utils.read_json('URL', dev_global.env.CONF_FILE))
    print("test read_url")
    print(utils.read_url('Sina', dev_global.env.CONF_FILE))
    print("test record_base")
    print(dev_global.env.LOG_FILE)
    utils.INFO('test')
    utils.ERROR('test')
    utils.WARN('test')
    print("Not tested: class Resource.")
    print("Not tested: str2number.")


def unit_test_network():
    network.delay(4)
    print('Network test finished.')


if __name__ == '__main__':
    unit_test_network()
    unit_test_utils()
