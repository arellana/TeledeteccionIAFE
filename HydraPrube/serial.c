#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <wiringPi.h>
#include <wiringSerial.h>

/*****************************************************************************/
void readLine(int fd) {
	while (serialDataAvail(fd)) {
		printf("%c", serialGetchar(fd));
	}
}

/*****************************************************************************/
int main() {
	int fd;
	char dat;

	// Setup serial port on ODROID
	if ((fd = serialOpen("/dev/ttyUSB0",9600)) < 0) {
		fprintf(stderr, "Unable to open serial device: %s\n", strerror(errno)) ;
		return 1 ;
	}

	if (wiringPiSetup() == -1) {
		fprintf(stdout, "Unable to start wiringPi: %s\n", strerror(errno)) ;
		return 1 ;
	}

	serialPrintf(fd, "000PE=1\r\n");
	delay(100);
	readLine(fd);
	delay(5000);

	for (int i = 0; i < 50; i++) {
		serialPrintf(fd, "000TR\r\n");
		delay(5000);

		serialPrintf(fd, "000T0\r\n");
		delay(100);
		readLine(fd);
		//delay(5000);
	}

	// while (serialDataAvail(fd) ) { 
	// 	dat = serialGetchar(fd);		/* receive character serially*/	
	// 	printf("%c", dat) ;
	// 	//fflush(stdout) ;
	// 	serialPutchar(fd, dat);		/* transmit character serially on port */
	// }

	// serialPrintf(fd,"\r"); // send enter key to read data from sensor
	//delay(1000);

	while (serialDataAvail(fd)) {
	printf("%c", serialGetchar(fd));
	}

	serialClose(fd);
}

