import { Controller, Get, OnModuleInit, UseInterceptors } from '@nestjs/common';
import { MessagePattern, Payload } from '@nestjs/microservices';
import { EmailCommand } from './commands/email.command';
import { SchemaRegistry } from '@kafkajs/confluent-schema-registry';

@Controller()
export class AppController {
  private schemaRegistry: SchemaRegistry;
  constructor(
  ) {
    /**
     * This function initializes the SchemaRegistry instance with the host and port of the Schema Registry service.
     */
    this.schemaRegistry = new SchemaRegistry({host: `http://${process.env.SCHEMA_REGISTRY_HOST}:${process.env.SCHEMA_REGISTRY_PORT}`});
  }


  @Get("/")
  getHello(): string {
    return "Hello World!";
  }

  @MessagePattern('send-email')
  async sendEmail(@Payload() data: any) {
    /**
     * This function decodes the data from the Kafka message and parses it into the EmailCommand object.
     * @param data The data from the Kafka message received as byte array.
     * @returns boolean
     */
    const parsedData:EmailCommand = await this.schemaRegistry.decode(data);
    console.log(parsedData);
    return true;
  }
}
