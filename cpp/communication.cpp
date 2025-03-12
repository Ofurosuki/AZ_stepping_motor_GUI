#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <unistd.h>

#include <array>
#include <communication.hpp>
#include <cstdint>
#include <cstring>
#include <iostream>

class Communication {
 private:
  uint16_t pos_0;
  uint16_t pos_1;
  uint16_t pos_2;
  uint16_t pos_3;
  uint32_t val;
  uint32_t upper_lim;
  uint32_t lower_lim;
  bool is_set_pos;
  std::string address;
  int port;
  int client;
  static constexpr int BUFSIZE = 4096;
  int frm_count;
  int current_position;
  int target_pos;

 public:
  Communication(std::string address, int port = 502)
      : pos_0(0),
        pos_1(0),
        pos_2(0),
        pos_3(0),
        val(0),
        upper_lim(333200),
        lower_lim(158650),
        is_set_pos(false),
        address(address),
        port(port),
        frm_count(0),
        current_position(0),
        target_pos(0) {
    std::cout << "***************************************" << std::endl;
    std::cout << "* Modbus TCP sample program for AZ series *" << std::endl;
    std::cout << "* C++ *" << std::endl;
    std::cout << "* *" << std::endl;
    std::cout << "***************************************" << std::endl;
    std::cout << "\nDriver IP Address >" << this->address << std::endl;
    std::cout << "\nDriver Port >" << this->port << std::endl;

    // Create socket
    this->client = socket(AF_INET, SOCK_STREAM, 0);

    // Set timeout
    struct timeval timeout;
    timeout.tv_sec = 5;
    timeout.tv_usec = 0;
    setsockopt(this->client, SOL_SOCKET, SO_RCVTIMEO, &timeout,
               sizeof(timeout));

    // Connect to driver
    struct sockaddr_in server_addr;
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(this->port);
    inet_aton(this->address.c_str(), &server_addr.sin_addr);

    if (connect(this->client, (struct sockaddr *)&server_addr,
                sizeof(server_addr)) < 0) {
      std::cerr << "Could not open socket." << std::endl;
      std::cerr << "  IPAddress: " << this->address << std::endl;
      std::cerr << "  Port: " << this->port << std::endl;
      exit(EXIT_FAILURE);
    }

    this->get_current_position();
    this->target_pos = this->get_current_position();
  }

  std::array<uint8_t, 4> decimal_to_hexadecimal(uint32_t value) {
    std::array<uint8_t, 4> byte_array;
    byte_array[0] = (value >> 24) & 0xFF;
    byte_array[1] = (value >> 16) & 0xFF;
    byte_array[2] = (value >> 8) & 0xFF;
    byte_array[3] = value & 0xFF;
    return byte_array;
  }

  int get_current_position() {
    std::array<uint8_t, 2> frm_count_array;
    memcpy(frm_count_array.data(), &frm_count, 2);
    std::array<uint8_t, 25> wkfrm;
    wkfrm.fill(0);
    std::copy(frm_count_array.begin(), frm_count_array.end(), wkfrm.begin());
    std::copy(packet_protocol::frm_Mon.begin(), packet_protocol::frm_Mon.end(),
              wkfrm.begin() + 2);

    // Send query
    send(this->client, wkfrm.data(), wkfrm.size(), 0);

    std::array<uint8_t, BUFSIZE> rcvData;
    recv(this->client, rcvData.data(), BUFSIZE, 0);

    this->current_position = (rcvData[19] << 24) | (rcvData[20] << 16) |
                             (rcvData[17] << 8) | rcvData[18];

    return this->current_position;
  }

  bool set_target_position(int target_pos) {
    if (target_pos > this->upper_lim || target_pos < this->lower_lim) {
      std::cout << "\x1b[31mTarget position is out of range\x1b[39m"
                << std::endl;
      return false;
    }
    this->is_set_pos = true;
    auto hex_values = decimal_to_hexadecimal(target_pos);
    this->pos_0 = hex_values[0];
    this->pos_1 = hex_values[1];
    this->pos_2 = hex_values[2];
    this->pos_3 = hex_values[3];
    this->target_pos = target_pos;
    return true;
  }

  void send_target_position() {
    if (!this->is_set_pos) {
      std::cout << "\x1b[31mPlease set target position first\x1b[39m"
                << std::endl;
      return;
    }

    std::array<uint8_t, 2> frm_count_array;
    memcpy(frm_count_array.data(), &frm_count, 2);
    std::array<uint8_t, 27> wkfrm;
    wkfrm.fill(0);
    std::copy(frm_count_array.begin(), frm_count_array.end(), wkfrm.begin());
    wkfrm[19] = this->pos_2;
    wkfrm[20] = this->pos_3;
    wkfrm[21] = this->pos_0;
    wkfrm[22] = this->pos_1;
    std::copy(packet_protocol::frm_ExeOpe.begin(),
              packet_protocol::frm_ExeOpe.end(), wkfrm.begin() + 2);

    // Send query
    send(this->client, wkfrm.data(), wkfrm.size(), 0);

    std::array<uint8_t, BUFSIZE> rcvData;
    recv(this->client, rcvData.data(), BUFSIZE, 0);

    std::cout << rcvData.data() << std::endl;
    this->frm_count++;
    usleep(100000);  // sleep for 0.1 seconds

    // Create query to turn off direct data drive trigger
    memcpy(frm_count_array.data(), &frm_count, 2);
    wkfrm.fill(0);
    std::copy(frm_count_array.begin(), frm_count_array.end(), wkfrm.begin());
    std::copy(packet_protocol::frm_ExeOpe_TrgOFF.begin(),
              packet_protocol::frm_ExeOpe_TrgOFF.end(), wkfrm.begin() + 2);

    // Send query
    send(this->client, wkfrm.data(), wkfrm.size(), 0);
    recv(this->client, rcvData.data(), BUFSIZE, 0);
  }

  int get_target_position() { return this->target_pos; }
};

int main() {
  Communication comm("your_driver_ip_address_here");
  comm.send_target_position();
  return 0;
}
