import { NestFactory } from '@nestjs/core';
import { Transport, MicroserviceOptions } from '@nestjs/microservices';
import { AppModule } from './app.module';


async function bootstrap() {
  const app = await NestFactory.createMicroservice<MicroserviceOptions>(
    AppModule,
    {
      transport: Transport.KAFKA,
      options: {
        client: {
          brokers: [`${process.env.KAFKA_HOST}:${process.env.KAFKA_PORT}`],
        }
      }
    },
  );

  await app.listen();
}
bootstrap();
