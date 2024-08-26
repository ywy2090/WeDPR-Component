package com.webank.wedpr.pir;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * @author zachma
 * @date 2024/8/18
 */
@SpringBootApplication
@EnableAutoConfiguration
public class WedprPirApplication {
    public static void main(String[] args) {
        SpringApplication.run(WedprPirApplication.class, args);
        System.out.println("Start WedprPirApplication Server successfully!");
    }
}
