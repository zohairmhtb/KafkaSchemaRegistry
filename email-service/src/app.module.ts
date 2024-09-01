import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { ClientsModule, Transport } from '@nestjs/microservices';

@Module({
  imports: [
    // ClientsModule.register([
    //   {
    //     name: 'KSR_EMAIL_SERVICE',
    //     transport: Transport.KAFKA,
    //     options: {
    //       client: {
    //         brokers: [`${process.env.KAFKA_HOST}:${process.env.KAFKA_PORT}`],
    //         clientId: 'ksr-email-service',
    //       },
    //       consumer: {
    //         groupId: 'ksr-email-service-consumer',
    //       },
    //     },
    //   },
    // ]),
  ],
  controllers: [AppController],
  providers: [],
})
export class AppModule {}
